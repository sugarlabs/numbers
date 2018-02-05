# globals
# g.py - globals for Numbers
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import pygame

import utils

XO = False  # affects the pygame.display.set_mode() call only
app = 'Numbers'
ver = '1.0'
ver = '1.1'
# lighter buttons - except "new"
# added new1() call when level changed
# event q cleared straight after animation
# new style g.py - all globals are initialised to empty
#                - then main() calls g.init() to give them their proper values
ver = '1.2'
# display moved up .5
# magician added
# improved score display
# load/save of level
ver = '1.3'
# can click on level marks
ver = '1.4'
# sugar cursor
ver = '1.5'
# uses copy.copy(rect) instead of rect.copy() in utils
ver = '1.6'  # <<< Release 3
# shows initial animation
ver = '1.7'
# utils with improved slider sensitivity
ver = '1.8'
# fixed for widescreen
# back button ok after correct
ver = '1.9'
# rationalised g.py
# removed Esc on XO
# no sound
ver = '2.0'
# sugar
ver = '3.0'
# redraw implemented
ver = '3.1'
# level 1 - all + or x
ver = '4.0'
# new sugar cursor etc
ver = '5.0'
# non-mouse version
# fake cursor
# target display interruptible
ver = '5.1'
# tablet version rather than keypad numbers
ver = '5.2'
# DOWN toggles auto mouse
ver = '5.3'
# state introduced = better control
ver = '5.4'
# back->up left->mouse_left
ver = '5.6'
# arrows -> mouse movement only
# M = toggle auto mouse
ver = '21'
# buffer flush when animation interrupted
ver = '22'
# key repeat with throttle added
ver = '23'
# button.py - do g.pos when mouse set
ver = '24'
# flush_queue() doesn't use gtk on non-XO
ver = '25'
# best added

UP = (264, 273)
DOWN = (258, 274)
LEFT = (260, 276)
RIGHT = (262, 275)
CROSS = (259, 120)
CIRCLE = (265, 111)
SQUARE = (263, 32)
TICK = (257, 13)


def init():  # called by main()
    global redraw
    global screen, w, h, font1, font2, clock
    global factor, offset, imgf, message, version_display
    global pos, pointer
    redraw = True
    version_display = False
    screen = pygame.display.get_surface()
    pygame.display.set_caption(app)
    screen.fill((70, 0, 70))
    pygame.display.flip()
    w, h = screen.get_size()
    if float(w) / float(h) > 1.5:  # widescreen
        offset = (w - 4 * h / 3) / 2  # we assume 4:3 - centre on widescreen
    else:
        h = int(.75 * w)  # allow for toolbar - works to 4:3
        offset = 0
    clock = pygame.time.Clock()
    factor = float(h) / 24  # measurement scaling factor (32x24 = design units)
    imgf = float(h) / 900  # image scaling factor - images built for 1200x900
    if pygame.font:
        t = int(64 * imgf)
        font1 = pygame.font.Font(None, t)
        t = int(72 * imgf)
        font2 = pygame.font.Font(None, t)
    message = ''
    pos = pygame.mouse.get_pos()
    pointer = utils.load_image('pointer.png', True)
    pygame.mouse.set_visible(False)

    # this activity only
    global sp, sp1, sp2
    global nos_k, signs, max_n, buffr, aim, top, level, score, best, best_c
    global magician, sparkle, target, smiley, plus, times, equals, n
    global n_glow, n_pale
    global xy1, cxy2, xy3, offset1, offset2, state
    sp = sy(.3)  # space between digits in single number
    sp1 = sy(2)  # space between numbers
    sp2 = sy(1.5)  # space between numbers and symbols
    nos_k = 3  # number of numbers offered
    signs = ('=', '+', '*')
    max_n = 5  # biggest number
    buffr = []
    aim = 0
    top = []
    level = 1
    score = 0
    best = 0
    equals = utils.load_image('equals.png', True)
    magician = utils.load_image('magician.png', True)
    sparkle = utils.load_image('sparkle.png', True)
    target = utils.load_image('target.png', True)
    smiley = utils.load_image('smiley.png', True)
    plus = utils.load_image('plus.png', True)
    times = utils.load_image('times.png', True)
    best_c = (sx(10.6), sy(20.2))
    n = []  # 0 to 9 images
    n_glow = []  # ... with glow
    n_pale = []
    for i in range(10):
        img = utils.load_image(str(i) + '.png', True)
        n.append(img)
        img = utils.load_image(str(i) + 'g.png', True)
        n_glow.append(img)
        img = utils.load_image(str(i) + 's.png', True)
        n_pale.append(img)
    xy1 = sx(3), sy(3.0)
    cxy2 = sx(4), sy(10)
    xy3 = sx(3), sy(13)
    ph2 = pointer.get_height() / 2
    offset1 = n[1].get_width() / 2, n[0].get_height() - ph2
    offset2 = 0, ph2
    state = 1  # 1 = top line; 2 = ops line; 3 = wrong; 4 = right


def sx(f):  # scale x function
    return int(f * factor) + offset


def sy(f):  # scale y function
    return int(f * factor)
