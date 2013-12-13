# utils.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import os
import sys
import copy
import random
import logging
import pygame

import g
import load_save

#constants
RED, BLUE, GREEN = (255, 0, 0), (0, 0, 255), (0, 255, 0)
BLACK, WHITE = (0, 0, 0), (255, 255, 255)
CYAN, ORANGE, CREAM = (0, 255, 255), (255, 165, 0), (255, 255, 192)
YELLOW = (255, 255, 0)


def exit():
    save()
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def save():
    dir = ''
    dir = os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir is None:
        dir = ''
    fname = os.path.join(dir, 'data', 'numbers.dat')
    f = open(fname,  'w')
    load_save.save(f)
    f.close


def load():
    dir = ''
    dir = os.environ.get('SUGAR_ACTIVITY_ROOT')
    if dir is None:
        dir = ''
    fname = os.path.join(dir, 'data', 'numbers.dat')
    try:
        f = open(fname,  'r')
    except Exception as e:
        logging.error('Could not open %s: %s' % (fname, e))
        return None
    try:
        load_save.load(f)
    except Exception as e:
        logging.error('load_save failed: %s' % (e))
    f.close


def version_display():
    g.message = g.app + ' ' + g.ver
    g.message += '  ' + str(g.screen.get_width()) + ' x ' + \
        str(g.screen.get_height())
    message(g.screen, g.font1, g.message)


# loads an image (eg pic.png) from the data subdirectory
# converts it for optimum display
# resizes it using the image scaling factor,  g.imgf
#   so it is the right size for the current screen resolution
#   all images are designed for 1200x900
def load_image(file1, alpha=False, subdir=''):  # eg subdir = 'glow'
    data = 'data'
    if subdir != '':
        data = os.path.join('data', subdir)
    fname = os.path.join(data, file1)
    try:
        img = pygame.image.load(fname)
    except:
        print "Peter says: Can't find " + fname
        exit()
    if alpha:
        img = img.convert_alpha()
    else:
        img = img.convert()
    if abs(g.imgf - 1.0) > .1:  # only scale if factor <> 1
        w = img.get_width()
        h = img.get_height()
        try:
            img = pygame.transform.smoothscale(
                img, (int(g.imgf * w), int(g.imgf * h)))
        except:
            img = pygame.transform.scale(
                img, (int(g.imgf * w), int(g.imgf * h)))
    return img


# eg new_list = copy_list(old_list)
def copy_list(l):
    new_list = []
    new_list.extend(l)
    return new_list


def shuffle(lst):
    l1 = lst
    lt = []
    for i in range(len(lst)):
        ln = len(l1)
        r = random.randint(0, ln - 1)
        lt.append(lst[r])
        l1.remove(lst[r])
    return lt


def centre_blit(screen, img, (cx, cy), angle=0):  # rotation is clockwise
    img1 = img
    if angle != 0:
        img1 = pygame.transform.rotate(img, -angle)
    rect = img1.get_rect()
    screen.blit(img1, (cx - rect.width / 2, cy - rect.height / 2))


def text_blit(screen, s, font, (cx, cy), (r, g, b)):
    text = font.render(s, True, (0, 0, 0))
    rect = text.get_rect()
    rect.centerx = cx + 2
    rect.centery = cy + 2
    screen.blit(text, rect)
    text = font.render(s, True, (r, g, b))
    rect = text.get_rect()
    rect.centerx = cx
    rect.centery = cy
    screen.blit(text, rect)
    return rect


def text_blit1(screen, s, font, (x, y), (r, g, b)):
    text = font.render(s, True, (r, g, b))
    rect = text.get_rect()
    rect.x = x
    rect.y = y
    screen.blit(text, rect)


# m is the message
# d is the # of pixels in the border around the text
# (cx, cy)  =  coords centre - (0, 0) means use screen centre
def message(screen, font, m, (cx, cy)=(0, 0), d=20):
    if m != '':
        if pygame.font:
            text = font.render(m, True, (255, 255, 255))
            shadow = font.render(m, True, (0, 0, 0))
            rect = text.get_rect()
            if cx == 0:
                cx = screen.get_width() / 2
            if cy == 0:
                cy = screen.get_height() / 2
            rect.centerx = cx
            rect.centery = cy
            bgd = pygame.Surface((rect.width + 2 * d, rect.height + 2 * d))
            bgd.fill((0, 255, 255))
            bgd.set_alpha(128)
            screen.blit(bgd, (rect.left - d, rect.top - d))
            screen.blit(
                shadow, (rect.x + 2, rect.y + 2, rect.width, rect.height))
            screen.blit(text, rect)


def mouse_on_img(img, (x, y)):  # x, y = top left
    w = img.get_width()
    h = img.get_height()
    mx, my = g.pos
    if mx < x:
        return False
    if mx > (x + w):
        return False
    if my < y:
        return False
    if my > (y + h):
        return False
    try:  # in case out of range
        col = img.get_at((int(mx - x), int(my - y)))
    except:
        return False
    if col[3] < 10:
        return False
    return True


def mouse_on_img1(img, (cx, cy)):
    xy = centre_to_top_left(img, (cx, cy))
    return mouse_on_img(img, xy)


def mouse_on_img_rect(img, (cx, cy)):
    w2 = img.get_width() / 2
    h2 = img.get_height() / 2
    x1 = cx - w2
    y1 = cy - h2
    x2 = cx + w2
    y2 = cy + h2
    return mouse_in(x1, y1, x2, y2)


def mouse_in(x1, y1, x2, y2):
    mx, my = g.pos
    if x1 > mx:
        return False
    if x2 < mx:
        return False
    if y1 > my:
        return False
    if y2 < my:
        return False
    return True


def mouse_in_rect(rect):  # x, y, w, h
    return mouse_in(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3])


def display_score():
    if pygame.font:
        text = g.font2.render(str(g.score), True, ORANGE, BLUE)
        w = text.get_width()
        h = text.get_height()
        x = g.sx(5.7)
        y = g.sy(18.8)
        d = g.sy(.3)
        pygame.draw.rect(g.screen, BLUE,
                         (x - d - g.sy(.05), y - d, w + 2 * d, h + 2 * d))
        g.screen.blit(text, (x, y))
        centre_blit(g.screen, g.sparkle,
                    (x - d + g.sy(.05), y + h / 2 - g.sy(.2)))


def display_number(n, (cx, cy), font, colour=BLACK, bgd=None,
                   outline_font=None):
    if pygame.font:
        if bgd is None:
            text = font.render(str(n), True, colour)
        else:
            text = font.render(str(n), True, colour, bgd)
        if outline_font is not None:
            outline = outline_font.render(str(n), True, BLACK)
            centre_blit(g.screen, outline, (cx, cy))
        centre_blit(g.screen, text, (cx, cy))


def display_number1(n, (x, cy), font, colour=BLACK):
    if pygame.font:
        text = font.render(str(n), True, colour)
        y = cy - text.get_height() / 2
        g.screen.blit(text, (x, y))


def top_left_to_centre(img, (x, y)):
    cx = x + img.get_width() / 2
    cy = y + img.get_height() / 2
    return (cx, cy)


def centre_to_top_left(img, (cx, cy)):
    x = cx - img.get_width() / 2
    y = cy - img.get_height() / 2
    return (x, y)
