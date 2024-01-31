import curses
import sys
import os
import copy
import random
from curses import textpad

username = "no name"

options = [
'''#.#
...
###''',
'''###
...
#.#''',
'''###
###
###''',
'''#.#
..#
#.#''',
'''#.#
#..
#.#''',
'''#.#
...
#.#''',
'''###
...
###''',
'''#.#
#.#
#.#''',
'''#.#
#..
###''',
'''#.#
..#
###''',
'''###
..#
#.#''',
'''###
#..
#.#''',
]

option_dim = 3

# possible neighors binary:  0      0       0       0
#                          north   east   south   west
neighbours = {
    0: "1101",
    1: "0111",
    2: "0000",
    3: "1011",
    4: "1110",
    5: "1111",
    6: "0101",
    7: "1010",
    8: "1100",
    9: "1001",
    10: "0011",
    11: "0110"
}

def write_highscores(highscore_file, score, username):
    if score > 0:
        highscores = []
        if os.path.exists(highscore_file):
            file = open(highscore_file, "r")
            highscores = file.read().splitlines()
            file.close()
        file = open(highscore_file, "w")
        highscores.append("{} - {}".format(score, username))
        highscores.sort(key=lambda x : int(x.split("-")[0]), reverse=True)
        file.write("\n".join(highscores))
        file.close()

def draw_score(score, stdscr, box):
    stdscr.addstr(box[0][0]-1, box[0][1], "score: {}".format(score))

def draw_player_lasers(player_lasers, max_lasers, stdscr, box):
    stdscr.addstr(box[0][0]-1, box[1][1] - 10, "ammo: {}/{}".format(player_lasers, max_lasers))

def draw_objects(objects, stdscr, ch, color):
    for y, x in objects:
        stdscr.addstr(y, x, ch, color)

def join_row(row, option_dim):
    row_strings = []
    result = ""
    for i in range(option_dim):
        for el in row:
            result += el.split("\n")[i]
        result += "\n"
    return result

def check_neighbours(grid_props, i, j, dim, dim_h):
    # check west east
    for k in range(-1, 2, 2):
        possible_neighbours = []
        ind_j = j + k
        if (0 <= ind_j < dim) and not grid_props[i][ind_j]["collapsed"]:
            curr_option = grid_props[i][j]["option"]
            curr_option_neighbours = list(neighbours[curr_option])
            for key in neighbours:
                value_split = list(neighbours[key])
                if value_split[(k % (option_dim + 1) + 2) % (option_dim + 1)] != curr_option_neighbours[k % (option_dim + 1)]:
                    if key in grid_props[i][ind_j]["possible_options"]:
                        grid_props[i][ind_j]["possible_options"].remove(key)
    # check north south
    for k in range(-1, 2, 2):
        possible_neighbours = []
        ind_i = i + k
        if (0 <= ind_i < dim_h) and not grid_props[ind_i][j]["collapsed"]:
            curr_option = grid_props[i][j]["option"]
            curr_option_neighbours = list(neighbours[curr_option])
            for key in neighbours:
                value_split = list(neighbours[key])
                if value_split[(k + 3) % (option_dim + 1)] != curr_option_neighbours[k + 1]:
                    if key in grid_props[ind_i][j]["possible_options"]:
                        grid_props[ind_i][j]["possible_options"].remove(key)

def find_new_neighbours(grid, grid_props):
    min_length = len(options)
    new_neighbours = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if not grid_props[i][j]["collapsed"] and len(grid_props[i][j]["possible_options"]) <= min_length:
                if len(grid_props[i][j]["possible_options"]) < min_length and len(grid_props[i][j]["possible_options"]) >= 0:
                    new_neighbours = [[i, j]]
                    min_length = len(grid_props[i][j]["possible_options"])
                elif len(grid_props[i][j]["possible_options"]) == min_length:
                    new_neighbours.append([i, j])
    return new_neighbours

def generate_grid(grid, grid_props, dim, dim_h):
    rand_option = random.choice(range(len(options)))
    i = random.choice(range(len(grid)))
    j = random.choice(range(len(grid[0])))
    while grid_props[i][j]["collapsed"]:
        i = random.choice(range(len(grid)))
        j = random.choice(range(len(grid[0])))
    grid[i][j] = options[rand_option]
    grid_props[i][j]["option"] = rand_option
    grid_props[i][j]["collapsed"] = True
    check_neighbours(grid_props, i, j, dim, dim_h)
    new_neighbours = find_new_neighbours(grid, grid_props)
    iteration = 0
    while (len(new_neighbours) > 0):
        iteration += 1
        rand_neighbour = random.choice(range(len(new_neighbours)))
        i = new_neighbours[rand_neighbour][0]
        j = new_neighbours[rand_neighbour][1]
        rand_option = random.choice(grid_props[i][j]["possible_options"])
        grid[i][j] = options[rand_option]
        grid_props[i][j]["option"] = rand_option
        grid_props[i][j]["collapsed"] = True
        check_neighbours(grid_props, i, j, dim, dim_h)
        new_neighbours = find_new_neighbours(grid, grid_props)

def init_grid(grid, grid_props, dim, dim_h):
    for i in range(dim_h):
        row = []
        grid_props.append([])
        for j in range(dim):
            row.append(options[2])
            grid_props[i].append({
                "collapsed": False,
                "option": 2,
                "possible_options": list(range(len(options)))
            })
        grid.append(row)

def grid_to_rows(grid, grid_rows_string, grid_rows_pos, box):
    i = 0
    for row in grid:
        for r in join_row(row, option_dim).split("\n"):
            grid_rows_string.append(r)
            grid_rows_pos.append([box[0][0] + i + 1, box[0][1] + 1])
            i += 1
        i -= 1

def row_to_objects(grid_rows_string, grid_rows_pos, obstacles, coins, ammo_boxes, add_box, missiles, add_missile):
    for i in range(len(grid_rows_string)):
        string_list = list(grid_rows_string[i])
        x_pos = 0
        for ch in string_list:
            if ch == "#":
                obstacles.insert(0, [grid_rows_pos[i][0], grid_rows_pos[i][1] + x_pos])
            elif add_box and ch == "." and random.random() < 0.001:
                ammo_boxes.insert(0, [grid_rows_pos[i][0], grid_rows_pos[i][1] + x_pos])
            elif add_missile and ch == "." and random.random() < 0.01:
                missiles.insert(0, {"pos": [grid_rows_pos[i][0], grid_rows_pos[i][1] + x_pos], "direction": curses.KEY_DOWN})
                coins.insert(0, [grid_rows_pos[i][0], grid_rows_pos[i][1] + x_pos])
            elif ch == ".":
                coins.insert(0, [grid_rows_pos[i][0], grid_rows_pos[i][1] + x_pos])
            x_pos += 1


# for debugging
# def main():
#     grid = []
#     grid_props = []
#     dim = 10
#     dim_h = 10

#     new_grid = []
#     new_grid_props = []
#     new_grid_rows_string = []
#     new_grid_rows_pos = []

#     init_grid(grid, grid_props, dim, dim_h)

#     generate_grid(grid, grid_props, dim, dim_h)

#     init_grid(new_grid, new_grid_props, dim, dim_h)

#     new_grid[-1] = grid[0]
#     new_grid_props[-1] = grid_props[0]

#     generate_grid(new_grid, new_grid_props, dim, dim_h)

#     new_grid.pop()
#     new_grid_props.pop()

#     for row in new_grid:
#         print(join_row(row, option_dim), end="")
#     print("----")
#     for row in grid:
#         print(join_row(row, option_dim), end="")

# main()

def main(stdscr):
    grid = []
    grid_props = []

    new_grid = []
    new_grid_props = []
    new_grid_rows_string = []
    new_grid_rows_pos = []

    player_color = 0
    obstacle_color = 0
    coin_color = 0
    laser_color = 0
    ammo_box_color = 0
    missile_color = 0

    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    if os.name != "nt":
        for i in range(0, curses.COLORS):
            curses.init_pair(i, i, -1)
        # random colors
        player_color = curses.color_pair(random.randrange(0, curses.COLORS-1))
        obstacle_color = curses.color_pair(random.randrange(0, curses.COLORS-1))
        coin_color = curses.color_pair(curses.COLOR_WHITE+1)
        laser_color = curses.color_pair(curses.COLOR_RED+1)
        ammo_box_color = curses.color_pair(random.randrange(0, curses.COLORS-1))
        missile_color = curses.color_pair(random.randrange(0, curses.COLORS-1))

    player_ch = '@'
    obstacle_ch = '#'
    coin_ch = '.'
    ammo_box_ch = '%'
    stdscr.erase()
    sh = 45
    sw = 90
    scr_sh, scr_sw = stdscr.getmaxyx()
    if scr_sh < sh or scr_sw < sw:
        sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh-3, sw-3]]

    dim = int((sw-6) / 3)
    dim_h = int(sh / 6 - 3)

    init_grid(grid, grid_props, dim, dim_h)

    generate_grid(grid, grid_props, dim, dim_h)

    init_grid(new_grid, new_grid_props, dim, dim_h)

    new_grid[-1] = grid[0]
    new_grid_props[-1] = grid_props[0]

    generate_grid(new_grid, new_grid_props, dim, dim_h)

    new_grid.pop()
    new_grid_props.pop()

    grid_to_rows(new_grid, new_grid_rows_string, new_grid_rows_pos, box)

    grid_rows_string = []
    grid_rows_pos = []

    grid_to_rows(grid, grid_rows_string, grid_rows_pos, box)

    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    startpos = [sh//2, sw//2]
    player = [[startpos[0], startpos[1]]]
    obstacles = []
    lasers = []
    coins = []
    ammo_boxes = []
    missiles = []

    row_to_objects(grid_rows_string, grid_rows_pos, obstacles, coins, ammo_boxes, False, missiles, False)

    score = 0
    highscore_file = "maze_runner_highscores.txt"
    direction = curses.KEY_UP
    dir_dict = {
        curses.KEY_RIGHT: [1, 1],
        curses.KEY_LEFT: [1, -1],
        curses.KEY_UP: [0, -1],
        curses.KEY_DOWN: [0, 1]
    }
    laser_ch_dict = {
        curses.KEY_RIGHT: "-",
        curses.KEY_LEFT: "-",
        curses.KEY_UP: "|",
        curses.KEY_DOWN: "|"
    }
    missile_ch_dict = {
        curses.KEY_RIGHT: ">",
        curses.KEY_LEFT: "<",
        curses.KEY_UP: "^",
        curses.KEY_DOWN: "v"
    }

    stdscr.nodelay(1)
    stdscr.timeout(1)
    max_speed = 100 if os.name != "nt" else 3
    max_speed_obstacles = 400 if os.name != "nt" else 16
    min_speed_obstacles = 200 if os.name != "nt" else 8
    max_speed_lasers = 30 if os.name != "nt" else 1
    max_speed_missiles = 50 if os.name != "nt" else 2
    counter_obstacles = 1
    counter_lasers = 1
    counter_missiles = 1
    max_lasers = 5
    player_lasers = max_lasers
    player_stop = False
    gameover = False
    paused = False
    counter = 1
    delete_grid_row = False
    can_shoot = True
    while 1:
        key = stdscr.getch()

        if not gameover and not paused:
            if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                player_copy = copy.deepcopy(player[0])
                player_copy[dir_dict[key][0]] += dir_dict[key][1]
                if player_copy not in obstacles:
                    direction = key


            if counter == 0:
                stdscr.erase()
                if not player_stop:
                    player[0][dir_dict[direction][0]] += dir_dict[direction][1]

            if counter_obstacles == 0:
                stdscr.erase()
                if len(new_grid_rows_pos) <= 3:
                    old_grid = copy.deepcopy(new_grid)
                    old_grid_props = copy.deepcopy(new_grid_props)
                    new_grid = []
                    new_grid_props = []
                    init_grid(new_grid, new_grid_props, dim, dim_h)
                    new_grid[-1] = old_grid[0]
                    new_grid_props[-1] = old_grid_props[0]
                    generate_grid(new_grid, new_grid_props, dim, dim_h)
                    new_grid_rows_pos = []
                    new_grid_rows_string = []
                    grid_to_rows(new_grid, new_grid_rows_string, new_grid_rows_pos, box)

                for i in range(len(grid_rows_pos)):
                    grid_rows_pos[i][0] += 1
                    if grid_rows_pos[i][0] == box[1][0]:
                        delete_grid_row = True
                new_grid_row_pos = new_grid_rows_pos.pop()
                new_grid_row_pos = [box[0][0] + 1, box[0][1] + 1]
                new_grid_row_string = new_grid_rows_string.pop()
                if new_grid_row_string == "":
                    new_grid_row_pos = new_grid_rows_pos.pop()
                    new_grid_row_pos = [box[0][0] + 1, box[0][1] + 1]
                    new_grid_row_string = new_grid_rows_string.pop()
                obstacle_row_pos = [box[0][0], box[0][1] + 1]
                grid_rows_pos.insert(0, new_grid_row_pos)
                grid_rows_string.insert(0, new_grid_row_string)
                row_to_objects([new_grid_row_string], [obstacle_row_pos], obstacles, coins, ammo_boxes, True, missiles, True)

                if delete_grid_row:
                    grid_rows_pos.pop()
                    grid_rows_string.pop()

                for obstacle in obstacles:
                    if obstacle[0] + 1 == box[1][0]:
                        obstacles.remove(obstacle)
                    else:
                        obstacle[0] += 1
                        if obstacle[1] == player[0][1] and obstacle[0] == player[0][0]:
                            # player_stop = True
                            if player[0][dir_dict[curses.KEY_DOWN][0]] + dir_dict[curses.KEY_DOWN][1] not in [box[0][0], box[0][1], box[1][0], box[1][1]]:
                                if player[0][0] in [box[0][0], box[1][0]] or player[0][1] in [box[0][1], box[1][1]]:
                                    stdscr.addstr(startpos[0], startpos[1]-10, 'Game Over')
                                    write_highscores(highscore_file, score, username)
                                    gameover = True
                for coin in coins:
                    if coin[0] + 1 == box[1][0]:
                        coins.remove(coin)
                    else:
                        coin[0] += 1

                for ammo_box in ammo_boxes:
                    if ammo_box[0] + 1 == box[1][0]:
                        ammo_boxes.remove(ammo_box)
                    else:
                        ammo_box[0] += 1

                player[0][dir_dict[curses.KEY_DOWN][0]] += dir_dict[curses.KEY_DOWN][1]
                for laser in lasers:
                    if laser["pos"][0] + 1 == box[1][0]:
                        laser.remove(laser)
                    else:
                        laser["pos"][dir_dict[curses.KEY_DOWN][0]] += dir_dict[curses.KEY_DOWN][1]
                for missile in missiles:
                    if missile["pos"][0] + 1 == box[1][0]:
                        missiles.remove(missile)
                    else:
                        missile["pos"][dir_dict[curses.KEY_DOWN][0]] += dir_dict[curses.KEY_DOWN][1]

            if counter_lasers == 0:
                stdscr.erase()
                can_shoot = True
                for laser in lasers:
                    laser["pos"][dir_dict[laser["direction"]][0]] += dir_dict[laser["direction"]][1]
                    if laser["pos"][0] in [box[0][0], box[1][0]] or laser["pos"][1] in [box[0][1], box[1][1]]:
                        lasers.remove(laser)
                        continue
                    if laser["pos"] in obstacles:
                        obstacles.remove(laser["pos"])
                        lasers.remove(laser)
                        continue
                    for missile in missiles:
                        if missile["pos"] == laser["pos"]:
                            missiles.remove(missile)
                            lasers.remove(laser)
                            continue

            if counter_missiles == 0:
                stdscr.erase()
                can_shoot = True
                for missile in missiles:
                    missile_copy = copy.deepcopy(missile)
                    missile_copy["pos"][dir_dict[missile_copy["direction"]][0]] += dir_dict[missile_copy["direction"]][1]
                    if missile_copy["pos"][0] in [box[0][0], box[1][0]] or missile_copy["pos"][1] in [box[0][1], box[1][1]]:
                        missiles.remove(missile)
                        continue
                    for laser in lasers:
                        if missile_copy["pos"] == laser["pos"]:
                            missiles.remove(missile)
                            lasers.remove(laser)
                            continue
                    possible_directions = []
                    opposite_direction = curses.KEY_DOWN
                    missile_copy["pos"][dir_dict[missile_copy["direction"]][0]] -= dir_dict[missile_copy["direction"]][1]
                    curr_m_dir = missile_copy["direction"]
                    for m_dir in list(dir_dict.keys()):
                        missile_copy["pos"][dir_dict[m_dir][0]] += dir_dict[m_dir][1]
                        if not (missile_copy["pos"] in obstacles or missile_copy["pos"][0] in [box[0][0], box[1][0]] or missile_copy["pos"][1] in [box[0][1], box[1][1]]):
                            if dir_dict[m_dir][0] != dir_dict[curr_m_dir][0] or m_dir == curr_m_dir:
                                possible_directions.append(m_dir)
                            else:
                                opposite_direction = m_dir
                        missile_copy["pos"][dir_dict[m_dir][0]] -= dir_dict[m_dir][1]

                    if len(possible_directions) > 0:
                        missile["direction"] = random.choice(possible_directions)
                    m_pos = missile["pos"].copy()
                    m_pos[dir_dict[missile["direction"]][0]] += dir_dict[missile["direction"]][1]
                    if m_pos in obstacles and len(possible_directions) == 0:
                        missile["direction"] = opposite_direction
                        # obstacles.remove(missile["pos"])
                        # missiles.remove(missile)
                    missile["pos"][dir_dict[missile["direction"]][0]] += dir_dict[missile["direction"]][1]


            draw_objects(obstacles, stdscr, obstacle_ch, obstacle_color)
            draw_objects(coins, stdscr, coin_ch, coin_color)
            draw_objects(ammo_boxes, stdscr, ammo_box_ch, ammo_box_color)

            textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])

            draw_objects(player, stdscr, player_ch, player_color)
            for laser in lasers:
                draw_objects([laser["pos"]], stdscr, laser_ch_dict[laser["direction"]], laser_color)

            for missile in missiles:
                try:
                    draw_objects([missile["pos"]], stdscr, missile_ch_dict[missile["direction"]], missile_color)
                except:
                    missiles.remove(missile)

            draw_objects(player, stdscr, player_ch, player_color)
            draw_score(score, stdscr, box)
            draw_player_lasers(player_lasers, max_lasers, stdscr, box)

            player_copy = copy.deepcopy(player[0])
            player_copy[dir_dict[direction][0]] += dir_dict[direction][1]

            if player[0] in coins:
                coins.remove(player[0])
                score += 1

            if player[0] in ammo_boxes:
                player_lasers = max_lasers
                ammo_boxes.remove(player[0])

            if player[0] in [missile["pos"] for missile in missiles]:
                stdscr.addstr(startpos[0], startpos[1]-10, 'Game Over')
                write_highscores(highscore_file, score, username)
                gameover = True

            if player_copy in obstacles:
                player_stop = True
            elif player_copy[0] in [box[0][0], box[1][0]] or player_copy[1] in [box[0][1], box[1][1]]:
                stdscr.addstr(startpos[0], startpos[1]-10, 'Game Over')
                write_highscores(highscore_file, score, username)
                gameover = True
            else:
                player_stop = False

            counter += 1
            counter %= max_speed
            counter_obstacles += 1
            counter_obstacles %= max_speed_obstacles
            counter_lasers += 1
            counter_lasers %= max_speed_lasers
            counter_missiles += 1
            counter_missiles %= max_speed_missiles
            if score > 0 and score % 50 == 0 and max_speed_obstacles > min_speed_obstacles:
                if os.name != "nt":
                    max_speed_obstacles -= 10
                else:
                    max_speed_obstacles -= 1
                score += 1

        if key == ord('f'):
            if can_shoot and player_lasers > 0:
                lasers.append({"pos": [player[0][0], player[0][1]], "direction": direction })
                player_lasers -= 1
                can_shoot = False
        if key == ord('q'):
            if not gameover:
                write_highscores(highscore_file, score, username)
            break
        if key == ord('r'):
            direction = curses.KEY_UP
            player = [[startpos[0], startpos[1]]]
            obstacles = []
            coins = []
            lasers = []
            missiles = []
            ammo_boxes = []
            stdscr.erase()
            score = 0
            counter = 1
            counter_obstacles = 1
            counter_lasers = 1
            counter_missiles = 1
            max_speed_obstacles = 400 if os.name != "nt" else 16
            player_lasers = max_lasers
            gameover = False
            grid = []
            grid_props = []
            new_grid = []
            new_grid_props = []
            new_grid_rows_string = []
            new_grid_rows_pos = []

            new_grid_rows_pos = []
            new_grid_rows_string = []

            init_grid(grid, grid_props, dim, dim_h)

            generate_grid(grid, grid_props, dim, dim_h)

            init_grid(new_grid, new_grid_props, dim, dim_h)

            new_grid[-1] = grid[0]
            new_grid_props[-1] = grid_props[0]

            generate_grid(new_grid, new_grid_props, dim, dim_h)

            new_grid.pop()
            new_grid_props.pop()

            grid_to_rows(new_grid, new_grid_rows_string, new_grid_rows_pos, box)

            grid_rows_string = []
            grid_rows_pos = []

            grid_to_rows(grid, grid_rows_string, grid_rows_pos, box)

            row_to_objects(grid_rows_string, grid_rows_pos, obstacles, coins, ammo_boxes, False, missiles, False)
        if key == ord('p'):
            if paused == False:
                paused = True
                stdscr.addstr(startpos[0], startpos[1]-6, 'Paused')
            else:
                paused = False
                stdscr.erase()

if len(sys.argv) < 2:
    username = input("Please provide your player name: ")
else:
    username = sys.argv[1]

curses.wrapper(main)
