#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PYTHON IMPORTS
#
import sys

#
# PANDA3D ENGINE IMPORTS
#
from pandac.PandaModules import WindowProperties

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


def hide_cursor():
    """set the Cursor invisible"""
    props = WindowProperties()
    props.setCursorHidden(True)
    # somehow the window gets undecorated after hiding the cursor
    # so we reset it here to the value we need
    # props.setUndecorated(settings.fullscreen)
    base.win.requestProperties(props)


def show_cursor():
    """set the Cursor visible again"""
    props = WindowProperties()
    props.setCursorHidden(False)
    # set the filename to the mouse cursor
    x11 = "assets/cursor.x11"
    win = "assets/cursor.ico"
    if sys.platform.startswith("linux"):
        props.setCursorFilename(x11)
    else:
        props.setCursorFilename(win)
    base.win.requestProperties(props)

def center_cursor():
    """Positions the cursor in the center of the screen"""
    win_width_half = base.win.getXSize() / 2
    win_height_half = base.win.getYSize() / 2
    base.win.movePointer(0, win_width_half, win_height_half)
