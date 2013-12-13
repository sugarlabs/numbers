# slider.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import copy
import pygame

import utils
import g


# sets g.level 1..steps
class Slider:
    def __init__(self, cx, cy, steps, colour=utils.BLACK):
        self.easy = utils.load_image('easy.png', True)
        self.hard = utils.load_image('hard.png', True)
        self.xo = utils.load_image('xo.png', True)
        iw = self.hard.get_width()
        ih = self.hard.get_height()
        w = g.sy(20)
        w2 = w / 2
        h2 = ih / 2
        self.x1 = cx - w2 + g.sy(.1)
        self.y = cy - h2
        self.x2 = cx + w2 - iw - g.sy(.2)
        x = cx - w2 + iw * 1.2
        w = w - 2 * iw * 1.2
        h = g.sy(.12)
        y = cy + g.sy(.34)
        self.rect = pygame.Rect(x, y, w, h)
        mh = g.sy(1)
        self.mark = pygame.Rect(x, y - mh / 2 + h / 2, h, mh)
        self.steps = steps
        self.dx = w / (steps - 1)
        self.colour = colour
        self.cx = cx
        self.cy = cy
        marks = []
        x = self.rect.left
        click_rects = []
        dx = self.dx
        for i in range(self.steps):
            rect = copy.copy(self.mark)
            rect.left = x - 5
            rect.width = 10
            marks.append(rect)
            click_rect = pygame.Rect(
                x - dx / 2, self.mark.top, dx, self.mark.h)
            click_rects.append(click_rect)
            x += dx
        self.marks = marks
        self.click_rects = click_rects

    def draw(self):
        g.screen.blit(self.easy, (self.x1, self.y))

        g.screen.blit(self.hard, (self.x2, self.y))
        pygame.draw.rect(g.screen, self.colour, self.rect)  # horizontal line
        x = self.rect.left  # now draw marks
        for i in range(self.steps):
            self.mark.left = x
            pygame.draw.rect(g.screen, self.colour, self.mark)
            if i == (g.level - 1):
                dx = self.xo.get_width() / 2
                dy = self.xo.get_height() / 2
                g.screen.blit(
                    self.xo, (x - dx + self.mark.w / 2, self.cy - dy))
            x += self.dx

    def mouse(self):
        mx, my = g.pos
        rect = self.easy.get_rect(topleft=(self.x1, self.y))
        if rect.collidepoint(mx, my):
            if g.level > 1:
                g.level -= 1
                return True
        rect = self.hard.get_rect(topleft=(self.x2, self.y))
        if rect.collidepoint(mx, my):
            if g.level < self.steps:
                g.level += 1
                return True
        n = 1
        for rect in self.click_rects:
            if rect.collidepoint(mx, my):
                if g.level == n:
                    return False
                else:
                    g.level = n
                    return True
            n += 1
        return False
