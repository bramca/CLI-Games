import curses
import random
import math
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
     "lshape_reverse": '''
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

def draw_score(score, stdscr, box):
    stdscr.addstr(box[0][0]-1, box[0][1], "score: {}".format(score))

def draw_objects(objects, stdscr, ch, color):
    for y, x in objects:
        stdscr.addstr(y, x, ch, color)

# def main():
#     sh = 30
#     sw = 30
#     box = [[3, 3], [sh-3, sw-3]]
#     shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], [box[0][0] + 1, sw // 2], "random_color")
#     print(shape)

# main()

def main(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i+1, i, -1)
    # random colors
    stdscr.clear()
    sh = 30
    sw = 30
    scr_sh, scr_sw = stdscr.getmaxyx()
    if scr_sh < sh or scr_sw < sw:
        sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh-3, sw-3]]
    startpos = [box[0][0] + 1, sw // 2]

    shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], startpos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
    obstacles = []

    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    score = 0

    direction = None
    dir_dict = {
        curses.KEY_RIGHT: [1, 1],
        curses.KEY_LEFT: [1, -1],
        curses.KEY_DOWN: [0, 1]
    }

    stdscr.nodelay(1)
    stdscr.timeout(1)
    counter = 1
    start_speed = 300
    curr_speed = start_speed
    max_speed = 50
    gameover = False
    paused = False
    while 1:
        # TODO: do line check and remove when horizontal line is full
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
                shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], startpos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
            if counter == 0:
                stdscr.erase()
                shape_copy = copy.deepcopy(shape)
                shape_copy.move_down()
                if not shape_copy.check_bounderies_down(box, obstacles):
                    shape.move_down()
                else:
                    for obj in shape.objects:
                        obstacles.append({"pos": obj["pos"], "ch": obj["ch"], "color": shape.color})

                    shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], startpos, curses.color_pair(random.randrange(0, curses.COLORS-1)))
                pass
            textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
            for obj in obstacles:
                draw_objects([obj["pos"]], stdscr, obj["ch"], obj["color"])
            for obj in shape.objects:
                draw_objects([obj["pos"]], stdscr, obj["ch"], shape.color)
            stdscr.refresh()
            counter += 1
            counter %= curr_speed

        if key == ord('q'):
            break
        if key == ord('r'):
            direction = None
            stdscr.erase()
            counter = 1
            curr_speed = start_speed
            score = 0
            shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], startpos, curses.color_pair(random.randrange(0, curses.COLORS-1)))

            gameover = False
        if key == ord('p'):
            if paused == False:
                paused = True
                stdscr.addstr(sh // 2, (sw // 2) - 3, 'Paused')
            else:
                paused = False
                stdscr.erase()

curses.wrapper(main)
