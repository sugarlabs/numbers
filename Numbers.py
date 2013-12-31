#!/usr/bin/python
# Numbers.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import sys
import random
from gi.repository import Gtk
import pygame

import g
import utils
import buttons
import slider
import load_save


class Numbers:

    def __init__(self, colors, sugar=False):
        self.colors = colors[:]
        self.sugar = sugar
        self.journal = True  # set to False if we come in via main()
        self.canvas = None

    def display(self):
        g.screen.fill(self.colors[1])
        if not self.sugar:
            g.screen.fill((255, 255, 192))
            g.screen.blit(g.magician, (g.sx(0), g.sy(18.0)))
        cx = g.sx(26)
        cy = g.sy(5.0)
        utils.centre_blit(g.screen, g.target, (cx, cy))

        if g.aim > 0:
            self.display_n_glow(g.aim, (cx, cy))
        x, y = g.xy1
        pale = False
        if g.state == 2:
            pale = True
        for i in range(len(g.top)):
            x = self.display_n(g.top[i], (x, y), True, False, pale)
            x += g.sp1
        x, y = g.xy3
        for i in range(len(g.buffr)):
            m = g.buffr[i]
            if m == 'plus':
                g.screen.blit(g.plus, (x, y))
                x += g.plus.get_width()
            elif m == 'times':
                g.screen.blit(g.times, (x, y))
                x += g.times.get_width()
            elif m == 'equals':
                g.screen.blit(g.equals, (x, y))
                x += g.equals.get_width()
            else:
                x = self.display_n(g.buffr[i], (x, y))
            x += g.sp2
        if len(g.top) == 0:
            buttons.off(['plus', 'times'])
        buttons.draw()
        if not self.sugar:
            self.slider.draw()
        if g.state == 4:
            utils.centre_blit(g.screen, g.smiley, (g.sx(16), g.sy(12)))
        if g.score > 0:
            self.display_score()
        if not self.sugar and g.best > 0:
            utils.text_blit(
                g.screen, str(g.best), g.font2, g.best_c, utils.ORANGE)

    # returns x of right edge
    def display_n(self, n, (x, y), display=True, glow=False, pale=False):
        s = str(n)
        for i in range(len(s)):
            n1 = int(s[i: i + 1])
            img = g.n[n1]
            if glow:
                img = g.n_glow[n1]
            if pale:
                img = g.n_pale[n1]
            if display:
                g.screen.blit(img, (x, y))
            x += g.n[n1].get_width() + g.sp
        return x - g.sp

    def display_n_glow(self, n, (cx, cy)):  # for target
        w = self.display_n(n, (0, 0), False)
        extra_w_for_glow = g.n_glow[0].get_width() - g.n[0].get_width()
        x = cx - (w + extra_w_for_glow) / 2
        h = g.n_glow[0].get_height()
        y = cy - h / 2
        self.display_n(n, (x, y), True, True)
        x = cx - w / 2
        h = g.n[0].get_height()
        y = cy - h / 2
        self.display_n(n, (x, y), True, False)

    def display_score(self):
        if self.sugar:
            self.label.set_markup(
                '<span><big><b> %s (%s)</b></big></span>' % (
                    str(int(g.score)), str(int(g.best))))
        else:
            text = g.font2.render(str(g.score), True, utils.ORANGE, utils.BLUE)
            w = text.get_width()
            h = text.get_height()
            x = g.sx(5.15)
            y = g.sy(19.6)
            d = g.sy(.3)
            pygame.draw.rect(g.screen, utils.BLUE,
                             (x - d, y - d, w + 2 * d, h + 2 * d - g.sy(.2)))
            g.screen.blit(text, (x, y))
            utils.centre_blit(g.screen, g.sparkle,
                              (x - d + g.sy(.05), y - d + g.sy(1.1)))

    def do_button(self, button):
        if button == 'equals':
            self.calc()
            buttons.off(['plus', 'times', 'equals'])
            if not self.complete():
                g.state = 1
                self.mouse_init()
        elif button == 'back':
            self.reset()
        elif button in ['new', 'green']:
            self.new1()
        else:
            g.buffr.append(button)
            buttons.off(['plus', 'times', 'equals'])
            g.state = 1
            self.mouse_init()

    def do_key(self, key):
        if key in g.CROSS:
            bu = buttons.check()
            if bu != '':
                self.do_button(bu)
                return
            if g.state == 1:
                self.check_numbers()
            return
        if key in g.UP:
            if self.back_button.mouse_on():
                if g.state == 1:
                    self.mouse_init()
            elif buttons.active('back'):
                buttons.set_mouse('back')
                if g.state == 2:
                    self.mouse_ind = 0
            return
        if key in g.DOWN:
            if buttons.active('back'):
                if g.state in (1, 3):
                    buttons.set_mouse('back')
            return
        if key in g.RIGHT:
            if not self.complete():
                self.mouse_right()
            return
        if key in g.LEFT:
            if not self.complete():
                self.mouse_left()
            return
        if key == pygame.K_m:
            self.mouse_auto = not self.mouse_auto
            self.mouse_init()
            return
        if key in g.SQUARE or key in g.CIRCLE:
            self.do_button('new')
            return
        if key in g.TICK:
            self.inc_level()
            return
        if key == pygame.K_v:
            g.version_display = not g.version_display
            return

    def mouse_init(self):
        self.mouse_ind = 0  # 1st number
        if g.state == 2:
            self.mouse_ind = 1  # plus
            if len(g.top) == 0:
                self.mouse_ind = 3  # equals
        self.mouse_set()

    def mouse_right(self):
        if self.mouse_ind is None:
            self.mouse_init()
            return
        if g.state == 1:
            self.mouse_right1()
            return
        if g.state == 2:
            self.mouse_right2()

    def mouse_left(self):
        if self.mouse_ind is None:
            self.mouse_init()
            return
        if g.state == 1:
            self.mouse_left1()
            return
        if g.state == 2:
            self.mouse_left2()

    def mouse_right1(self):  # used for state 1
        self.mouse_ind += 1
        if self.mouse_ind == len(g.top):
            self.mouse_ind = 0
        self.mouse_set()

    def mouse_left1(self):  # used for state 1
        self.mouse_ind -= 1
        if self.mouse_ind < 0:
            self.mouse_ind = len(g.top) - 1
        self.mouse_set()

    def mouse_right2(self):  # used for states 2 & 3
        for i in range(5):  # no infinite loop
            self.mouse_ind += 1
            if self.mouse_ind == len(self.ops):
                self.mouse_ind = 0
            if buttons.active(self.ops[self.mouse_ind]):
                self.mouse_set()
                return

    def mouse_left2(self):  # used for states 2 & 3
        for i in range(5):  # no infinite loop
            self.mouse_ind -= 1
            if self.mouse_ind < 0:
                self.mouse_ind = len(self.ops) - 1
            if buttons.active(self.ops[self.mouse_ind]):
                self.mouse_set()
                return

    def mouse_set(self):
        if not self.mouse_auto:
            return
        if g.state == 1:  # top line
            x1, y1 = g.xy1
            dx, dy = g.offset1
            for i in range(self.mouse_ind):
                x = self.display_n(g.top[i], (x1, y1), False)
                x1 = x + g.sp1
            x1 += dx
            y1 += dy
            pygame.mouse.set_pos(x1, y1)
            g.pos = (x1, y1)
            return
        elif g.state == 2:  # ops line
            if self.mouse_auto:
                buttons.set_mouse(self.ops[self.mouse_ind])

    def inc_level(self):
        g.level += 1
        if g.level > self.slider.steps:
            g.level = 1
        self.level1()

    def reset(self):
        g.state = 1
        g.top = utils.copy_list(g.nos)
        g.buffr = []
        buttons.off(['plus', 'times', 'equals'])
        buttons.off('back')
        self.mouse_init()

    def calc(self):
        a = []
        for i in range(len(g.buffr)):
            if g.buffr[i] == 'times':
                ind = len(a) - 1
                a[ind] *= g.buffr[i + 1]
                g.buffr[i + 1] = 'ignore'
            elif g.buffr[i] == 'ignore':
                pass
            elif g.buffr[i] != 'plus':
                a.append(g.buffr[i])
        n = 0
        for i in range(len(a)):
            n += a[i]
        g.buffr = []
        g.top.append(n)

    def check_numbers(self):
        if g.state == 1:
            mx, my = g.pos
            x1, y1 = g.xy1
            h = g.n[0].get_height()
            for i in range(len(g.top)):
                x = self.display_n(g.top[i], (x1, y1), False)
                w = x - x1
                rect = pygame.Rect(x1, y1, w, h)
                if rect.collidepoint(mx, my):
                    g.buffr.append(g.top[i])
                    del g.top[i]
                    buttons.on(['plus', 'times'])
                    buttons.on('back')
                    g.state = 2
                    self.mouse_init()
                    if len(g.buffr) > 1:
                        buttons.on('equals')
                    return True
                x1 = x + g.sp1
        return False

    def gen_nos(self):
        l = []
        for i in range(g.nos_k):
            l.append(random.randint(1, g.max_n))
        return l

    def gen_aim(self):
        l = utils.copy_list(g.nos)
        #shuffle nos
        lt = utils.shuffle(l)
        #generate answer
        buff = ""
        r = random.randint(1, 2)  # for level 1
        while True:
            n = lt[0]
            lt.remove(n)
            buff += str(n)
            if len(lt) == 0:
                break
            if g.level > 1:
                r = random.randint(0, 2)
            if g.signs[r] == '=':
                n = eval(buff)
                buff = ""
                lt.append(n)
                lt = utils.shuffle(lt)
            else:
                buff = buff + g.signs[r]
        return eval(buff)

    def new1(self):
        g.nos = self.gen_nos()
        g.aim = self.gen_aim()
        g.top = utils.copy_list(g.nos)
        g.buffr = []
        buttons.off(['plus', 'times', 'equals'])
        buttons.off('back')
        g.state = 1
        self.mouse_init()
        self.anim_start()
        self.scored = False

    def anim_start(self):  # have g.nos and g.aim
        self.anim_ms = pygame.time.get_ticks()
        self.anim_i = 0
        self.anim_aim = g.aim
        g.aim = 0
        # for target display
        self.anim_mx = 1
        for i in range(g.nos_k):
            self.anim_mx *= g.max_n
        self.anim_tn = 0
        g.top = []

    def anim_update(self):
        if self.anim_i < len(g.nos):
            g.top = g.nos[:self.anim_i + 1]
            self.anim_i += 1
        else:
            self.anim_tn += 1
            if self.anim_tn == 15:
                self.anim_end()
                return
            g.aim = random.randint(5, self.anim_mx)

    def anim_end(self):
        if self.anim_ms is None:
            return
        g.top = utils.copy_list(g.nos)
        g.aim = self.anim_aim
        self.anim_ms = None

    def animation(self):
        if self.anim_ms is None:
            return
        d = pygame.time.get_ticks() - self.anim_ms
        if d > 150:  # delay in ms
            self.anim_ms = pygame.time.get_ticks()
            self.anim_update()
            g.redraw = True

    def complete(self):
        if g.state in (3, 4):
            return True
        if len(g.buffr) == 0 and len(g.top) == 1:
            if g.aim in g.top:
                g.state = 4  # right
                if not self.scored:
                    self.scored = True
                    g.score += g.level
                    if g.score > g.best:
                        g.best = g.score
            else:
                g.state = 3  # wrong
            if self.mouse_auto:
                buttons.set_mouse('back')
            return True
        return False

    def reload(self):
        self.save_score = g.score
        buttons.reset()
        g.init()

    def set_label(self, label):
        self.label = label

    def set_buttons(self, green):
        self.green_button = green

    def level1(self, level=None):
        if level is not None:
            g.level = level
        g.nos_k = 3
        l = g.level
        if l > 5:
            g.nos_k = 4
            l -= 5
        g.max_n = l + 4
        self.new1()

    def flush_queue(self):
        flushing = True
        while flushing:
            flushing = False
            if self.journal:
                while Gtk.events_pending():
                    Gtk.main_iteration()
            for event in pygame.event.get():
                flushing = True

    def run(self, restore=False):
        self.black = False
        g.init()
        if not self.journal:
            utils.load()
        load_save.retrieve()
        x = g.sx(26)
        y = g.sy(11.2)
        if not self.sugar:
            buttons.Button("new", (x, y))
        x, y = g.cxy2
        dx = g.sy(4)
        self.back_button = buttons.Button("back", (x, y))
        x += dx
        buttons.Button("plus", (x, y))
        x += dx
        buttons.Button("times", (x, y))
        x += dx
        buttons.Button("equals", (x, y))
        self.ops = ['back', 'plus', 'times', 'equals']
        if not self.sugar:
            self.slider = slider.Slider(g.sx(22.4), g.sy(20.5), 10,
                                        utils.GREEN)
        self.mouse_auto = True
        self.anim_ms = None

        self.level1()  # initial animation
        self.scored = False
        if restore:
            g.score = self.save_score
        ctrl = False
        pygame.key.set_repeat(600, 120)
        key_ms = pygame.time.get_ticks()
        going = True
        if self.canvas is not None:
            self.canvas.grab_focus()
        while going:
            if self.journal:
                # Pump GTK messages.
                while Gtk.events_pending():
                    Gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if not self.journal:
                        utils.save()
                    going = False
                elif event.type == pygame.MOUSEMOTION:
                    g.pos = event.pos
                    g.redraw = True
                    if self.canvas is not None:
                        self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw = True
                    self.anim_end()
                    if event.button == 1:
                        bu = buttons.check()
                        if bu == '':
                            if not self.check_numbers():
                                if not self.sugar:
                                    if self.slider.mouse():
                                        self.level1()
                        else:
                            self.do_button(bu)  # eg do_button('plus')
                    self.flush_queue()
                elif event.type == pygame.KEYDOWN:
                    self.anim_end()
                    # throttle keyboard repeat
                    if pygame.time.get_ticks() - key_ms > 110:
                        key_ms = pygame.time.get_ticks()
                        if ctrl:
                            if event.key == pygame.K_q:
                                if not self.journal:
                                    utils.save()
                                going = False
                                break
                            else:
                                ctrl = False
                        if event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                            ctrl = True
                            break
                        self.do_key(event.key)
                        g.redraw = True
                        self.flush_queue()
                elif event.type == pygame.KEYUP:
                    ctrl = False
            if not going:
                break
            self.animation()
            if g.redraw:
                self.display()
                if g.version_display:
                    utils.version_display()
                if not self.black:
                    g.screen.blit(g.pointer, g.pos)
                pygame.display.flip()
                g.redraw = False
            g.clock.tick(40)


if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((1024, 768), pygame.FULLSCREEN)
    game = Numbers(([0, 255, 255], [0, 0, 0]))
    game.journal = False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
