# load_save.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g
import logging

loaded = []  # list of strings


def load(f):
    global loaded
    try:
        for line in f.readlines():
            loaded.append(line)
    except Exception as e:
        logging.error('Could not readlines: %s' % (e))


def save(f):
    f.write(str(int(g.level)) + '\n')
    f.write(str(int(g.best)) + '\n')


# note need for rstrip() on strings
def retrieve():
    global loaded
    if len(loaded) == 1:
        g.level = int(float(loaded[0].strip()))
    if len(loaded) > 1:
        g.best = int(float(loaded[1].strip()))
