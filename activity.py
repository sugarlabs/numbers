# activity.py
# my standard link between sugar and my activity
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""

from gettext import gettext as _
import logging
import gtk
import pygame

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityToolbarButton
from sugar.activity.widgets import StopButton
from sugar.graphics.toolbarbox import ToolbarButton
from sugar.graphics.toolbutton import ToolButton
from sugar.graphics.style import GRID_CELL_SIZE
from sugar import profile

import sugargame.canvas
import load_save
import Numbers


class PeterActivity(activity.Activity):
    LOWER = 1
    UPPER = 10

    def __init__(self, handle):
        super(PeterActivity, self).__init__(handle)

        # Get user's Sugar colors
        sugarcolors = profile.get_color().to_string().split(',')
        colors = [[int(sugarcolors[0][1:3], 16),
                   int(sugarcolors[0][3:5], 16),
                   int(sugarcolors[0][5:7], 16)],
                  [int(sugarcolors[1][1:3], 16),
                   int(sugarcolors[1][3:5], 16),
                   int(sugarcolors[1][5:7], 16)]]

        # No sharing
        self.max_participants = 1

        # Build the activity toolbar.
        toolbox = ToolbarBox()

        activity_button = ActivityToolbarButton(self)
        toolbox.toolbar.insert(activity_button, 0)
        activity_button.show()

        self._add_level_slider(toolbox.toolbar)

        green = ToolButton('green')
        toolbox.toolbar.insert(green, -1)
        green.set_tooltip(_('Run'))
        green.connect('clicked', self._button_cb, 'green')
        green.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = True
        toolbox.toolbar.insert(separator, -1)
        separator.show()

        label = gtk.Label('')
        label.set_use_markup(True)
        label.show()
        labelitem = gtk.ToolItem()
        labelitem.add(label)
        toolbox.toolbar.insert(labelitem, -1)
        labelitem.show()

        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbox.toolbar.insert(separator, -1)
        separator.show()

        stop = ToolButton('activity-stop')
        toolbox.toolbar.insert(stop, -1)
        stop.props.tooltip = _('Stop')
        stop.props.accelerator = '<Ctrl>Q'
        stop.connect('clicked', self.__stop_button_clicked_cb, activity)
        stop.show()

        toolbox.show()
        self.set_toolbox(toolbox)

        # Create the game instance.
        self.game = Numbers.Numbers(colors, sugar=True)

        # Build the Pygame canvas.
        self._pygamecanvas = sugargame.canvas.PygameCanvas(self)
        # Note that set_canvas implicitly calls
        # read_file when resuming from the Journal.
        self.set_canvas(self._pygamecanvas)
        self.game.canvas = self._pygamecanvas
        self.game.set_buttons(green)
        self.game.set_label(label)

        gtk.gdk.screen_get_default().connect('size-changed',
                                             self.__configure_cb)

        # Start the game running.
        self._pygamecanvas.run_pygame(self.game.run)

    def __stop_button_clicked_cb(self, button, activity):
        pygame.display.quit()
        pygame.quit()
        self.close()

    def __configure_cb(self, event):
        ''' Screen size has changed '''
        logging.debug(self._pygamecanvas.get_allocation())
        pygame.display.set_mode((gtk.gdk.screen_width(),
                                 gtk.gdk.screen_height() - GRID_CELL_SIZE),
                                pygame.RESIZABLE)

        self.game.reload()
        self._level_range.set_value(1)
        self.game.run(restore=True)

    def read_file(self, file_path):
        try:
            f = open(file_path, 'r')
        except Exception as e:
            logging.error('Could not open %s: %s' % (file_path, e))
            return
        load_save.load(f)
        f.close()

    def write_file(self, file_path):
        f = open(file_path, 'w')
        load_save.save(f)
        f.close()

    def _button_cb(self, button=None, color=None):
        self.game.do_button(color)

    def _add_level_slider(self, toolbar):
        self._level_stepper_down = ToolButton('easy')
        self._level_stepper_down.set_tooltip(_('Easier'))
        self._level_stepper_down.connect('clicked',
                                         self._level_stepper_down_cb)
        self._level_stepper_down.show()

        self._adjustment = gtk.Adjustment(
            1, self.LOWER, self.UPPER, 1, 5, 0)
        self._adjustment.connect('value_changed', self._level_change_cb)
        self._level_range = gtk.HScale(self._adjustment)
        self._level_range.set_draw_value(False)
        self._level_range.set_update_policy(gtk.UPDATE_CONTINUOUS)
        self._level_range.set_size_request(120, 15)
        self._level_range.show()

        self._level_stepper_up = ToolButton('hard')
        self._level_stepper_up.set_tooltip(_('Harder'))
        self._level_stepper_up.connect('clicked', self._level_stepper_up_cb)
        self._level_stepper_up.show()

        self._level_range_tool = gtk.ToolItem()
        self._level_range_tool.add(self._level_range)
        self._level_range_tool.show()

        toolbar.insert(self._level_stepper_down, -1)
        toolbar.insert(self._level_range_tool, -1)
        toolbar.insert(self._level_stepper_up, -1)
        return

    def _level_stepper_down_cb(self, button=None):
        new_value = self._level_range.get_value() - 1
        if new_value <= self.UPPER:
            self._level_range.set_value(new_value)
        else:
            self._level_range.set_value(self.UPPER)

    def _level_stepper_up_cb(self, button=None):
        new_value = self._level_range.get_value() + 1
        if new_value >= self.LOWER:
            self._level_range.set_value(new_value)
        else:
            self._level_range.set_value(self.LOWER)

    def _level_change_cb(self, button=None):
        logging.debug(self._adjustment.value)
        self.game.level1(level=self._adjustment.value)
        return True
