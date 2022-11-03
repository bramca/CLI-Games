import curses
import random
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
            else:
                object = {
                    "ch": ch,
                    "pos": [y, x]
                }
                self.objects.append(object)
                x += 1
    def __str__(self):
        result = "startpos: {}\nshape:\n{}\nobjects:".format(self.pos, self.shape)
        for obj in self.objects:
            result += "\npos: {}, ch: {}".format(obj["pos"], obj["ch"])
        return result

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

    shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], [box[0][0] + 1, sw // 2], curses.color_pair(random.randrange(0, curses.COLORS-1)))

    textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
    score = 0

    direction = None
    dir_dict = {
        curses.KEY_RIGHT: [1, 1],
        curses.KEY_LEFT: [1, -1],
        curses.KEY_UP: [0, -1],
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
        key = stdscr.getch()
        if not gameover and not paused:
            if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_UP, curses.KEY_DOWN]:
                # TODO: move object to correct place and do boundery check
                pass
            if counter == 0:
                stdscr.erase()
                # TODO: move object down and do correct boundery and line check
                pass
            textpad.rectangle(stdscr, box[0][0], box[0][1], box[1][0], box[1][1])
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
            shape = Shape(SHAPES[random.choice(list(SHAPES.keys()))], [box[0][0] + 1, sw // 2], curses.color_pair(random.randrange(0, curses.COLORS-1)))

            gameover = False
        if key == ord('p'):
            if paused == False:
                paused = True
            else:
                paused = False
                stdscr.erase()

curses.wrapper(main)
