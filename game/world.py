#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM

# Game imports
from core import helper
from worlds.forest import Level
from player.Player import Player

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class World(DirectObject, FSM):
    def __init__(self):
        FSM.__init__(self, "FSM-World")
        helper.hide_cursor()

        self.player = Player(base.cTrav)

    def start(self):
        self.request("Main")

    def stop(self):
        """Stop all game components and ignores all events"""
        helper.show_cursor()
        self.request("Quit")
        self.player.stopPlayer()
        self.ignoreAll()

    def enterMain(self):
        """Main state of the world."""
        print _("Enter World")
        helper.hide_cursor()
        self.level = Level()
        self.player.startPlayer()
        startPoint = self.level.getStartPoint()
        if startPoint is not None:
            self.player.setStartPos(startPoint.getPos())
            self.player.setStartHpr(startPoint.getHpr())
        self.player.centerCamera()
        self.player.centerCamera()

    def exitMain(self):
        print _("Exit World")
        helper.show_cursor()
        self.player.pausePlayer()
        self.level.stop()
        del self.level
