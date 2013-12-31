# buttons.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import pygame

import g
import utils


class Button:
    _instances = []

    def __init__(self, name, (x1, y1), centre=True):  # eg ('plus',(30,40))
        self._instances.append(self)
        up = utils.load_image(name + "_up.png", True)
        down = utils.load_image(name + "_down.png", True)
        w = up.get_width()
        h = up.get_height()
        x = x1
        y = y1
        if centre:
            self.cx = x
            self.cy = y
            x = x - w / 2
            y = y - h / 2
        else:
            self.cx = x + w / 2
            self.cy = y + h / 2
        self.rect = pygame.Rect(x, y, w, h)
        self.name = name
        self.x = x
        self.y = y
        self.active = True
        self.up = up
        self.down = down
        self.stay_down = False

    def mouse_on(self):
        mx, my = g.pos
        return self.rect.collidepoint(mx, my)

    def draw_up(self):
        g.screen.blit(self.up, (self.x, self.y))

    def draw_down(self):
        g.screen.blit(self.down, (self.x, self.y))

    def on(self):
        self.active = True

    def off(self):
        self.active = False


def draw():
    for b in Button._instances:
        if b.active:
            if b.stay_down:
                b.draw_down()
            else:
                b.draw_up()


def check():
    clear()
    for b in Button._instances:
        if b.active:
            if b.mouse_on():
                if b.name in ('xyz1', 'xyz2'):
                    b.stay_down = True
                else:
                    b.draw_down()
                    g.screen.blit(g.pointer, g.pos)
                    pygame.display.flip()
                    pygame.time.wait(300)
                return b.name
    return ''  # no button pressed


def clear():
    for b in Button._instances:
        b.stay_down = False


def active(name):
    for b in Button._instances:
        if b.name == name:
            return b.active
    return False  # not found


def stay_down(name):
    for b in Button._instances:
        if b.name == name:
            b.stay_down = True
            return
    return


def mouse_on(name):
    mx, my = g.pos
    for b in Button._instances:
        if b.name == name:
            return b.rect.collidepoint(mx, my)
    return False


def set_mouse(name):
    p2 = g.pointer.get_height() / 2
    for b in Button._instances:
        if b.name == name:
            x = b.cx
            y = b.cy + p2
            pygame.mouse.set_pos(x, y)
            g.pos = (x, y)


# eg1 buttons.on('plus')
# eg2 buttons.on(['plus','times'])
def on(name):
    if isinstance(name, str):
        list1 = []
        list1.append(name)
    else:
        list1 = name
    for b in Button._instances:
        if b.name in list1:
            b.active = True


# eg1 buttons.off('plus')
# eg2 buttons.off(['plus','times'])
def off(name):
    if isinstance(name, str):
        list1 = []
        list1.append(name)
    else:
        list1 = name
    for b in Button._instances:
        if b.name in list1:
            b.active = False
