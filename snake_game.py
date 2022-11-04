import curses
import random
import os.path
import sys
from curses import textpad

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


def draw_objects(objects, stdscr, ch, color):
    for y, x in objects:
        stdscr.addstr(y, x, ch, color)

def main(stdscr):
    username = sys.argv[1]
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i+1, i, -1)
    # random colors
    snake_color = curses.color_pair(random.randrange(0, curses.COLORS-1))
    food_color = curses.color_pair(random.randrange(0, curses.COLORS-1))
    superfood_color = curses.color_pair(random.randrange(0, curses.COLORS-1))
    obstacle_color = curses.color_pair(random.randrange(0, curses.COLORS-1))

    # fixed colors
    # snake_color = curses.color_pair(curses.COLOR_GREEN+1)
    # food_color = curses.color_pair(curses.COLOR_YELLOW+1)
    # superfood_color = curses.color_pair(curses.COLOR_RED+1)
    # obstacle_color = curses.color_pair(curses.COLOR_BLUE+1)
    snake_ch = '#'
    food_ch = '*'
    superfood_ch = '%'
    obstacle_ch = '&'
    stdscr.clear()
    sh = 45
    sw = 90
    scr_sh, scr_sw = stdscr.getmaxyx()
    if scr_sh < sh or scr_sw < sw:
        sh, sw = stdscr.getmaxyx()
    # sh = 50
    # sw = 140
    box = [[3, 3], [sh-3, sw-3]]

    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    startpos = [sh//2, sw//2]
    startlength = 15
    snake = []
    score = 0
    for i in range(startlength):
        snake.append([startpos[0], startpos[1]-i])
    food = []
    superfood = []
    obstacles = []
    obstacle_size = 40
    max_obstacles = 40
    obstaclecounter_speed = 100
    superfood_weight = 5
    foodcounter_speed = 2000
    superfoodcounter_speed = 4500
    direction = curses.KEY_RIGHT
    dir_dict = {
        curses.KEY_RIGHT: [1, 1],
        curses.KEY_LEFT: [1, -1],
        curses.KEY_UP: [0, -1],
        curses.KEY_DOWN: [0, 1]
    }

    stdscr.nodelay(1)
    stdscr.timeout(1)
    counter = 0
    foodcounter = 1
    superfoodcounter = 1
    obstaclecounter = 1
    max_speed = 60
    gameover = False
    paused = False
    highscore_file = "snake_highscores.txt"
    while 1:
        key = stdscr.getch()
        # stdscr.addstr(4, 4, "snake_color: {}".format(snake_color))
        # stdscr.addstr(5, 4, "food_color: {}".format(food_color))
        # stdscr.addstr(6, 4, "superfood_color: {}".format(superfood_color))
        # stdscr.addstr(7, 4, "obstacle_color: {}".format(obstacle_color))
        if not gameover and not paused:
            if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                temp_new_head = snake[0].copy()
                temp_new_head[dir_dict[key][0]] += dir_dict[key][1]
                if temp_new_head[0] != snake[1][0] or temp_new_head[1] != snake[1][1]:
                    direction = key
            if obstaclecounter == 0 and len(obstacles) < (obstacle_size * max_obstacles):
                if len(obstacles) % obstacle_size == 0 or not obstacles:
                    obstacle_new_head = [random.randrange(box[0][0]+1, box[1][0]-1), random.randrange(box[0][1]+1, box[1][1]-1)]
                    while obstacle_new_head in snake or obstacle_new_head in food:
                        obstacle_new_head = [random.randrange(box[0][0]+1, box[1][0]-1), random.randrange(box[0][1]+1, box[1][1]-1)]
                else:
                    obstacle_dir = random.choice(list(dir_dict.keys()))
                    obstacle_new_head = obstacles[0].copy()
                    obstacle_new_head[dir_dict[obstacle_dir][0]] += dir_dict[obstacle_dir][1]
                    while obstacle_new_head[0] in [box[0][0], box[1][0]] or obstacle_new_head[1] in [box[0][1], box[1][1]] or obstacle_new_head in snake:
                        obstacle_dir = random.choice(list(dir_dict.keys()))
                        obstacle_new_head = obstacles[0].copy()
                        obstacle_new_head[dir_dict[obstacle_dir][0]] += dir_dict[obstacle_dir][1]
                obstacles.insert(0, obstacle_new_head)
            if foodcounter == 0:
                new_food = [random.randrange(box[0][0]+1, box[1][0]-1), random.randrange(box[0][1]+1, box[1][1]-1)]
                while new_food in obstacles or new_food in snake:
                    new_food = [random.randrange(box[0][0]+1, box[1][0]-1), random.randrange(box[0][1]+1, box[1][1]-1)]
                food.append(new_food)
            if superfoodcounter == 0:
                superfood.append([random.randrange(box[0][0]+1, box[1][0]-1), random.randrange(box[0][1]+1, box[1][1]-1)])
            if counter == 0:
                new_head = snake[0].copy()
                new_head[dir_dict[direction][0]] += dir_dict[direction][1]
                snake.insert(0, new_head)
                snake.pop()
                stdscr.erase()
            if snake[0] in food:
                food.remove(snake[0])
                new_tail = snake[-1].copy()
                snake.append(new_tail)
                score += 1
            if snake[0] in superfood:
                superfood.remove(snake[0])
                new_tail = [snake[-1].copy() for i in range(superfood_weight)]
                snake += new_tail
                score += superfood_weight
            if snake[0][0] in [box[0][0], box[1][0]] or snake[0][1] in [box[0][1], box[1][1]] or snake[0] in snake[1:-1] or snake[0] in obstacles:
                stdscr.addstr(startpos[0], startpos[1]-10, 'Game Over')
                gameover = True
                write_highscores(highscore_file, score, username)
            textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
            draw_objects(snake, stdscr, snake_ch, snake_color)
            draw_objects(food, stdscr, food_ch, food_color)
            draw_objects(superfood, stdscr, superfood_ch, superfood_color)
            draw_score(score, stdscr, box)
            draw_objects(obstacles, stdscr, obstacle_ch, obstacle_color)
            stdscr.refresh()
            counter += 1
            counter %= max_speed
            foodcounter += 1
            foodcounter %= foodcounter_speed
            superfoodcounter += 1
            superfoodcounter %= superfoodcounter_speed
            obstaclecounter += 1
            obstaclecounter %= obstaclecounter_speed

        if key == ord('q'):
            write_highscores(highscore_file, score, username)
            break
        if key == ord('r'):
            direction = curses.KEY_RIGHT
            snake = []
            food = []
            superfood = []
            obstacles = []
            for i in range(startlength):
                snake.append([startpos[0], startpos[1]-i])
            stdscr.erase()
            counter = 0
            foodcounter = 1
            superfoodcounter = 1
            obstaclecounter = 1
            score = 0
            gameover = False
        if key == ord('p'):
            if paused == False:
                paused = True
                stdscr.addstr(startpos[0], startpos[1]-6, 'Paused')
            else:
                paused = False
                stdscr.erase()

curses.wrapper(main)
