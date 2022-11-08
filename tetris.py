import curses
import random
import math
import sys
import os
import copy
from curses import textpad
import re

SHAPES = {
    "line": '''
#
#
#
#''',
    "lshape": '''
##
 #
 #''',
     "lshape_reversed": '''
##
#
#''',
     "zshape": '''
#
##
 #''',
      "zshape_reversed": '''
 #
##
#''',
      "block": '''
##
##''',
      "tshape": '''
 #
###'''
}

class Shape:
    def __init__(self, shape, startpos, color):
        shape = re.sub(r"^\n", "", shape)
        self.shape = shape
        self.pos = startpos
        self.color = color
        self.objects = []
        y, x = startpos
        for ch in self.shape:
            if ch == "\n":
                y += 1
                x = self.pos[1]
            elif ch == "#":
                object = {
                    "ch": ch,
                    "pos": [y, x]
                }
                self.objects.append(object)
                x += 1
            else:
                x += 1
    def __str__(self):
        result = "startpos: {}\nshape:\n{}\nobjects:".format(self.pos, self.shape)
        for obj in self.objects:
            result += "\npos: {}, ch: {}".format(obj["pos"], obj["ch"])
        return result
    def check_bounderies_down(self, box, obstacles):
        for obj in self.objects:
            if obj["pos"] in [obs["pos"] for obs in obstacles] or obj["pos"][0] == box[1][0]:
                return True
        return False
    def check_bounderies_up(self, box, obstacles):
        for obj in self.objects:
            if obj["pos"] in [obs["pos"] for obs in obstacles] or obj["pos"][0] == box[0][0]:
                return True
        return False
    def check_bounderies_sides(self, box, obstacles):
        for obj in self.objects:
            if obj["pos"] in [obs["pos"] for obs in obstacles] or obj["pos"][1] in [box[0][1], box[1][1]] or obj["pos"][0] == box[1][0]:
                return True
        return False
    def move_down(self):
        for obj in self.objects:
            obj["pos"][0] += 1
    def move(self, direction, amount):
        for obj in self.objects:
            obj["pos"][direction] += amount
    def rotate(self, pivot, angle):
        pivot_obj = self.objects[pivot]
        for i in range(len(self.objects)):
            obj = self.objects[i]
            if i != pivot:
                x_old = obj["pos"][1] - pivot_obj["pos"][1]
                y_old = obj["pos"][0] - pivot_obj["pos"][0]
                x_new = x_old * int(math.cos(angle)) - y_old * int(math.sin(angle))
                y_new = x_old * int(math.sin(angle)) + y_old * int(math.cos(angle))
                obj["pos"][1] = x_new + pivot_obj["pos"][1]
                obj["pos"][0] = y_new + pivot_obj["pos"][0]

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

def draw_score(score, next_level, stdscr, box):
    stdscr.addstr(box[0][0] + 1, box[0][1] + 1, "score")
    stdscr.addstr(box[0][0] + 2, box[1][1] - len(str(score)), str(score))
    stdscr.addstr(box[0][0] + 3, box[0][1] + 1, "level")
    level = int(next_level / 150)
    stdscr.addstr(box[0][0] + 4, box[1][1] - len(str(level)), str(level))

def draw_objects(objects, stdscr, ch, color):
    for y, x in objects:
        stdscr.addstr(y, x, ch, color)

def check_lines(obstacles, max_chars):
    lines = {}
    for obs in obstacles:
        if lines.get(obs["pos"][0]):
            if obs not in lines.get(obs["pos"][0]):
                lines.get(obs["pos"][0]).append(obs)
        else:
            lines[obs["pos"][0]] = [obs]
    lines_removed = 0
    for y_pos in sorted(list(lines.keys()), reverse=True):
        for obs in lines[y_pos]:
            obs["pos"][0] += lines_removed
        if len(lines[y_pos]) == max_chars:
            for obs in lines[y_pos]:
                obstacles.remove(obs)
            lines_removed += 1
    return lines_removed

# def main():
#     sh = 30
#     sw = 30
#     box = [[3, 3], [sh-3, sw-3]]
#     shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], [box[0][0] + 1, sw // 2], "random_color")
#     print(shape)

# main()

def main(stdscr):
    username = sys.argv[1]
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    if os.name != "nt":
        for i in range(0, curses.COLORS):
            curses.init_pair(i+1, i, -1)
    # random colors
    stdscr.clear()
    sh = 25
    sw = 20
    scr_sh, scr_sw = stdscr.getmaxyx()
    if scr_sh < sh or scr_sw < sw:
        sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh-3, sw-3]]
    startpos = [box[0][0] + 1, sw // 2]
    next_shape_box = [[3, sw - 2], [8, sw+4]]
    next_shape_pos = [next_shape_box[0][0] + 1, next_shape_box[0][1]+2]
    score_box = [[next_shape_box[1][0], next_shape_box[0][1]], [next_shape_box[1][0] + 5, next_shape_box[1][1]]]

    # fixed colors
    shape_colors = {
        "line": 0,
        "lshape": 0,
        "lshape_reversed": 0,
        "zshape": 0,
        "zshape_reversed": 0,
        "block": 0,
        "tshape": 0
    }
    if os.name != "nt":
        shape_colors = {
            "line": curses.color_pair(curses.COLOR_RED+1),
            "lshape": curses.color_pair(curses.COLOR_YELLOW+1),
            "lshape_reversed": curses.color_pair(curses.COLOR_WHITE+1),
            "zshape": curses.color_pair(curses.COLOR_CYAN+1),
            "zshape_reversed": curses.color_pair(curses.COLOR_MAGENTA+1),
            "block": curses.color_pair(curses.COLOR_BLUE+1),
            "tshape": curses.color_pair(curses.COLOR_GREEN+1)
        }


    # shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], startpos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
    # next_shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], next_shape_pos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
    random_shape = random.choice(list(SHAPES.keys()))
    shape = Shape(SHAPES[random_shape], startpos, shape_colors[random_shape])
    random_shape = random.choice(list(SHAPES.keys()))
    next_shape = Shape(SHAPES[random_shape], next_shape_pos, shape_colors[random_shape])
    obstacles = []
    max_chars = 13

    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    textpad.rectangle(stdscr, score_box[0][0], score_box[0][1], score_box[1][0], score_box[1][1])
    textpad.rectangle(stdscr, next_shape_box[0][0], next_shape_box[0][1], next_shape_box[1][0], next_shape_box[1][1])
    score = 0
    scoring = [4, 10, 30, 120]
    highscore_file = "tetris_highscores.txt"
    direction = None
    dir_dict = {
        curses.KEY_RIGHT: [1, 1],
        curses.KEY_LEFT: [1, -1],
        curses.KEY_DOWN: [0, 1]
    }

    stdscr.nodelay(1)
    stdscr.timeout(1)
    counter = 1
    start_speed = 300 if os.name != "nt" else 12
    curr_speed = start_speed
    next_level = 150
    max_speed = 50 if os.name != "nt" else 2
    gameover = False
    paused = False
    while 1:
        key = stdscr.getch()
        if not gameover and not paused:
            if key in list(dir_dict.keys()):
                shape_copy = copy.deepcopy(shape)
                shape_copy.move(dir_dict[key][0], dir_dict[key][1])
                if not shape_copy.check_bounderies_sides(box, obstacles):
                    stdscr.erase()
                    shape.move(dir_dict[key][0], dir_dict[key][1])
                pass
            if key == curses.KEY_UP:
                shape_copy = copy.deepcopy(shape)
                shape_copy.rotate(2, math.pi / 2)
                if not shape_copy.check_bounderies_sides(box, obstacles):
                    stdscr.erase()
                    shape.rotate(2, math.pi / 2)
            if key == ord(' '):
                stdscr.erase()
                shape_copy = copy.deepcopy(shape)
                shape_copy.move_down()
                while not shape_copy.check_bounderies_down(box, obstacles):
                    shape.move_down()
                    shape_copy = copy.deepcopy(shape)
                    shape_copy.move_down()
                for obj in shape.objects:
                    obstacles.append({"pos": obj["pos"], "ch": obj["ch"], "color": shape.color})
                n_lines = check_lines(obstacles, max_chars)
                if n_lines > 0:
                    score += scoring[n_lines - 1]
                    if score >= next_level and curr_speed > max_speed:
                        if os.name != "nt":
                            curr_speed -= 10
                        else:
                            curr_speed -= 1
                        next_level += 150

                shape = Shape(next_shape.shape, startpos, next_shape.color)
                # next_shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], next_shape_pos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
                random_shape = random.choice(list(SHAPES.keys()))
                next_shape = Shape(SHAPES[random_shape], next_shape_pos, shape_colors[random_shape])
            if counter == 0:
                stdscr.erase()
                shape_copy = copy.deepcopy(shape)
                shape_copy.move_down()
                if not shape_copy.check_bounderies_down(box, obstacles):
                    shape.move_down()
                else:
                    for obj in shape.objects:
                        obstacles.append({"pos": obj["pos"], "ch": obj["ch"], "color": shape.color})
                    n_lines = check_lines(obstacles, max_chars)
                    if n_lines > 0:
                        score += scoring[n_lines - 1]
                        if score >= next_level and curr_speed > max_speed:
                            curr_speed -= 10
                            next_level += 150

                    shape = Shape(next_shape.shape, startpos, next_shape.color)
                    # next_shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], next_shape_pos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
                    random_shape = random.choice(list(SHAPES.keys()))
                    next_shape = Shape(SHAPES[random_shape], next_shape_pos, shape_colors[random_shape])
                pass
            textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
            textpad.rectangle(stdscr, score_box[0][0], score_box[0][1], score_box[1][0], score_box[1][1])
            textpad.rectangle(stdscr, next_shape_box[0][0], next_shape_box[0][1], next_shape_box[1][0], next_shape_box[1][1])
            draw_score(score, next_level, stdscr, score_box)
            for obj in obstacles:
                draw_objects([obj["pos"]], stdscr, obj["ch"], obj["color"])
            for obj in shape.objects:
                draw_objects([obj["pos"]], stdscr, obj["ch"], shape.color)
            for obj in next_shape.objects:
                draw_objects([obj["pos"]], stdscr, obj["ch"], next_shape.color)
            counter += 1
            counter %= curr_speed

            if shape.check_bounderies_up(box, obstacles):
                stdscr.addstr(sh // 2, (sw // 2)-4, 'Game Over')
                gameover = True
                write_highscores(highscore_file, score, username)

        if key == ord('q'):
            if not gameover:
                write_highscores(highscore_file, score, username)
            break
        if key == ord('r'):
            direction = None
            stdscr.erase()
            counter = 1
            curr_speed = start_speed
            next_level = 150
            score = 0
            # shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], startpos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
            # next_shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], next_shape_pos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
            random_shape = random.choice(list(SHAPES.keys()))
            shape = Shape(SHAPES[random_shape], startpos, shape_colors[random_shape])
            random_shape = random.choice(list(SHAPES.keys()))
            next_shape = Shape(SHAPES[random_shape], next_shape_pos, shape_colors[random_shape])
            obstacles = []

            gameover = False
        if key == ord('p'):
            if paused == False:
                paused = True
                stdscr.addstr(sh // 2, (sw // 2) - 3, 'Paused')
            else:
                paused = False
                stdscr.erase()

curses.wrapper(main)
