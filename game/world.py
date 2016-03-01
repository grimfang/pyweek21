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
        self.player.startPlayer()
        self.player.pausePlayer()
        self.player.hide()

        self.hud = HUD()

        self.level = Level(self.player)
        self.level.hide()

        def createFadeableImage(img, tsName, big=False):
            cm = CardMaker("FadableCard")
            cm.setFrame(-1, 1, -1, 1)
            image = NodePath(cm.generate())
            image.setTransparency(TransparencyAttrib.MAlpha)
            imageTex = loader.loadTexture(img)
            imageTs = TextureStage(tsName)
            imageTs.setMode(TextureStage.MReplace)
            image.setTexture(imageTs, imageTex)
            image.reparentTo(render2d)
            if big:
                image.setScale(0.75)
            else:
                image.setScale(0.5)
            image.setPos(0, 0, 0.25)
            image.hide()
            return image

        self.tutorial1 = createFadeableImage("gui/tutorial.png", "ts-tutorial1")
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

        self.intro1 = createFadeableImage("gui/intro1.png", "ts-intro1", True)
        self.intro2 = createFadeableImage("gui/intro1.png", "ts-intro2", True)
        self.intro3 = createFadeableImage("gui/intro1.png", "ts-intro3", True)
        self.tut1 = createFadeableImage("gui/intro2.png", "ts-tut1", True)
        self.tut2 = createFadeableImage("gui/intro2.png", "ts-tut2", True)
        self.introSequence = Sequence(
            Wait(1.0),
            Func(self.hud.showStory),
            Func(self.intro1.show),
            Func(self.hud.setStory, _("The Fire spirits set a big fire in the wood and burned down most of the plants")),
            self.intro1.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.intro1.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.intro1.hide),
            Func(self.intro2.show),
            Func(self.hud.setStory, _("Though rain has come and estinguished the fire.")),
            self.intro2.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.intro2.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.intro2.hide),
            Func(self.intro3.show),
            Func(self.hud.setStory, _("Now, in the aftermath of the fire, it's up to you to let new plants grow!")),
            self.intro3.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.intro3.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.intro3.hide),
            Func(self.tut1.show),
            Func(self.hud.setStory, _("Use W, A, S, D and the mouse to control the character")),
            self.tut1.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.tut1.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.tut1.hide),
            Func(self.tut2.show),
            Func(self.hud.setStory, _("Press Pos 1 to center the camera behind the player")),
            self.tut2.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.tut2.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.tut2.hide),
            Func(self.hud.hideStory),
            Func(self.demand, "Main"))

        self.acceptOnce("CharacterCollisions-in-tutorial1", self.showTutorial)
        self.accept("CharacterCollisions-in-PlantGroundCollider", self.enablePlanting)
        self.accept("CharacterCollisions-out-PlantGroundCollider", self.disablePlanting)
        self.accept("CharacterCollisions-in", self.checkCollisions)
        self.accept("player-plant_seed", self.doPlantSeed)
        self.accept("f1", self.showTutorial, extraArgs=[None])

    def start(self):
        self.request("Main")
        self.request("Intro")

    def stop(self):
        """Stop all game components and ignores all events"""
        helper.show_cursor()
        self.ignoreAll()
        self.player.stopPlayer()
        self.level.stop()
        del self.level
        self.tutorialInterval.finish()
        self.tutorial1.removeNode()
        self.hud.cleanup()

    def requestEscape(self):
        if self.state == "Intro":
            self.request("Main")
            return False
        else:
            return True

    def showTutorial(self, args):
        if not self.tutorialInterval.isPlaying():
            self.tutorialInterval.start()

    def checkCollisions(self, args):
        if "seedSphere" in args.getIntoNode().getName():
            self.doPickupSeed(args)

    def enablePlanting(self, args):
        self.currentPlantingGround = args.getIntoNode()
        self.player.enablePlanting(True)
        self.hud.showCanPlant()

    def disablePlanting(self, args):
        self.player.enablePlanting(False)
        self.hud.hideCanPlant()

    def doPickupSeed(self, args):
        self.player.doPickupSeed(args)
        self.level.doPickupSeed(args)

    def doPlantSeed(self):
        self.level.doPlantSeed(self.currentPlantingGround)

    def enterMain(self):
        """Main state of the world."""
        print _("Enter World")
        self.level.show()
        self.player.show()
        self.hud.show()
        self.player.resumePlayer()
        startPoint = self.level.getStartPoint()
        if startPoint is not None:
            self.player.setStartPos(startPoint.getPos())
            self.player.setStartHpr(startPoint.getHpr())
        helper.center_cursor()
        self.player.centerCamera()

    def exitMain(self):
        print _("Exit World")
        self.hud.hide()
        self.player.pausePlayer()

    def enterIntro(self):
        self.player.showCharFront()
        self.introSequence.start()

    def exitIntro(self):
        helper.center_cursor()
        self.player.centerCamera()
        self.introSequence.finish()
