#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from direct.showbase.DirectObject import DirectObject
from direct.fsm.FSM import FSM
from panda3d.core import (
    CardMaker,
    NodePath,
    TransparencyAttrib,
    TextureStage,)
from direct.interval.FunctionInterval import (
    Wait,
    Func)
from direct.interval.IntervalGlobal import Sequence

# Game imports
from core import helper
from worlds.forest import Level
from player.Player import Player
from gui.hud import HUD

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
        self.hud = HUD()

        cm = CardMaker("FadableCard")
        cm.setFrame(-1, 1, -1, 1)
        self.tutorial1 = NodePath(cm.generate())
        self.tutorial1.setTransparency(TransparencyAttrib.MAlpha)
        self.tutorial1Tex = loader.loadTexture("gui/tutorial.png")
        self.tutorial1Ts = TextureStage("ts-tutorial1")
        self.tutorial1Ts.setMode(TextureStage.MReplace)
        self.tutorial1.setTexture(self.tutorial1Ts, self.tutorial1Tex)
        self.tutorial1.reparentTo(render2d)
        self.tutorial1.setScale(0.5)
        self.tutorial1.setPos(0, 0, 0.25)
        self.tutorial1.hide()

        self.tutorialInterval = Sequence(
            Func(self.tutorial1.show),
            self.tutorial1.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(3.0),
            self.tutorial1.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.tutorial1.hide))

        self.acceptOnce("CharacterCollisions-in-tutorial1", self.showTutorial)
        self.accept("CharacterCollisions-in-PlantGroundCollider", self.enablePlanting)
        self.accept("CharacterCollisions-out-PlantGroundCollider", self.disablePlanting)
        self.accept("CharacterCollisions-in", self.checkCollisions)
        self.accept("f1", self.showTutorial, extraArgs=[None])

    def start(self):
        self.request("Main")

    def stop(self):
        """Stop all game components and ignores all events"""
        helper.show_cursor()
        self.request("Quit")
        self.player.stopPlayer()
        self.ignoreAll()
        self.tutorialInterval.finish()
        self.tutorial1.removeNode()
        self.hud.cleanup()

    def showTutorial(self, args):
        if not self.tutorialInterval.isPlaying():
            self.tutorialInterval.start()

    def checkCollisions(self, args):
        if "seedSphere" in args.getIntoNode().getName():
            self.doPickupSeed(args)

    def enablePlanting(self, args):
        self.currentPlantingGround = args
        self.player.enablePlanting(True)
        self.hud.showCanPlant()

    def disablePlanting(self, args):
        self.player.enablePlanting(False)
        self.hud.hideCanPlant()

    def doPickupSeed(self, args):
        self.player.doPickupSeed(args)
        self.level.doPickupSeed(args)

    def enterMain(self):
        """Main state of the world."""
        print _("Enter World")
        helper.hide_cursor()
        self.level = Level(self.player)
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
