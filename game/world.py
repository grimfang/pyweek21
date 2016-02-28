#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM

# Game imports
from core import helper
from worlds.dev_level import DevLevel

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class World(DirectObject, FSM):
    def __init__(self):
        FSM.__init__(self, "FSM-World")
        helper.hide_cursor()

        #TODO: Add game world logic
        self.devLevel = DevLevel()
        print render.ls()

    def stop(self):
        """Stop all game components and ignores all events"""
        helper.show_cursor()
        self.ignoreAll()

    def enterMain(self):
        """Main state of the world."""
        helper.hide_cursor()
        print _("Enter World")

    def exitMain(self):
        helper.show_cursor()
        print _("Exit World")
