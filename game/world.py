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

        self.points = 0
        self.water = 100

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

        self.tutorial1 = createFadeableImage("gui/tutorial3.png", "ts-tut3")
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
            Func(self.tutorial1.hide),
            name="Planting Tutorial Sequence")

        self.intro1 = createFadeableImage("gui/intro1.png", "ts-intro1", True)
        self.intro2 = createFadeableImage("gui/intro2.png", "ts-intro2", True)
        self.intro3 = createFadeableImage("gui/intro3.png", "ts-intro3", True)
        self.tut1 = createFadeableImage("gui/tutorial1.png", "ts-tut1", True)
        self.tut2 = createFadeableImage("gui/tutorial2.png", "ts-tut2", True)
        self.introSequence = Sequence(
            Wait(1.0),
            Func(self.hud.showStory),
            Func(self.intro1.show),
            Func(self.hud.setStory, _("Fire spirits set the forest alight, burning most of the trees and plants...")),
            self.intro1.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(8.0),
            self.intro1.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.intro1.hide),
            Func(self.intro2.show),
            Func(self.hud.setStory, _("Soon though rain came and estinguished the raging fires...")),
            self.intro2.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(8.0),
            self.intro2.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.intro2.hide),
            Func(self.intro3.show),
            Func(self.hud.setStory, _("A devastating aftermath, it's now up to you to help the forest regrow!")),
            self.intro3.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(8.0),
            self.intro3.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.intro3.hide),
            Func(self.tut1.show),
            Func(self.hud.setStory, _("Use W, A, S, D and the mouse to control the character.")),
            self.tut1.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(8.0),
            self.tut1.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.tut1.hide),
            Func(self.tut2.show),
            Func(self.hud.setStory, _("Press Home to center the camera behind the player.")),
            self.tut2.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(6.0),
            self.tut2.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.tut2.hide),
            Func(self.hud.hideStory),
            Func(self.demand, "Main"),
            name="Intro Sequence",)

        self.outro1 = createFadeableImage("gui/outro1.png", "ts-outro1", True)
        self.outro2 = createFadeableImage("gui/outro2.png", "ts-outro2", True)
        self.outro3 = createFadeableImage("gui/gameOver1.png", "ts-outro3", True)
        self.outroSequence = Sequence(
            Wait(1.0),
            Func(self.hud.showStory),
            Func(self.outro1.show),
            Func(self.hud.setStory, _("You have done well my little droplets.")),
            self.outro1.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.outro1.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.outro1.hide),
            Func(self.outro2.show),
            Func(self.hud.setStory, _("But... now it's again time to go for you.")),
            #Func(self.player.hide),
            self.outro2.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.outro2.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.outro2.hide),
            Func(self.outro3.show),
            Func(self.setEndingStoryText),
            self.outro3.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(10.0),
            self.outro3.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.outro3.hide),
            Func(self.hud.hideStory),
            Func(base.messenger.send, "GameOver"),
            name="Outro Sequence",)


        self.gameOver1 = createFadeableImage("gui/gameOver1.png", "ts-gameOver1", True)
        self.gameOverSequence = Sequence(
            Wait(1.0),
            Func(self.hud.showStory),
            Func(self.outro1.show),
            Func(self.hud.setStory, _("You did your best and now you're one with the nature.")),
            self.gameOver1.colorScaleInterval(
                1.5,
                (0,0,0,1),
                (0,0,0,0)),
            Wait(5.0),
            self.gameOver1.colorScaleInterval(
                1.5,
                (0,0,0,0),
                (0,0,0,1)),
            Func(self.gameOver1.hide),
            Func(self.hud.hideStory),
            Func(base.messenger.send, "GameOver"),
            name="Game Over Sequence",)

        # collision events
        self.acceptOnce("CharacterCollisions-in-tutorial1", self.showTutorial)
        self.acceptOnce("CharacterCollisions-in-finish", self.finishGame)
        self.accept("CharacterCollisions-in-PlantGroundCollider", self.enablePlanting)
        self.accept("CharacterCollisions-out-PlantGroundCollider", self.disablePlanting)
        self.accept("CharacterCollisions-in", self.checkCollisions)

        # Speeking with other Droplets
        self.accept("CharacterCollisions-in-Speek_AlmostDone", self.showText, extraArgs=[_("You almost reached the end")])
        self.accept("CharacterCollisions-out-Speek_AlmostDone", self.hideText)
        self.accept("CharacterCollisions-in-Speek_Hi", self.showText, extraArgs=[_("Hi!")])
        self.accept("CharacterCollisions-out-Speek_Hi", self.hideText)
        self.accept("CharacterCollisions-in-Speek_NoSeeds", self.theFriendlyDroplet)
        self.accept("CharacterCollisions-out-Speek_NoSeeds", self.hideText)
        self.accept("CharacterCollisions-in-Speek_PlantHere", self.showText, extraArgs=[_("Go on, plant a seed here!")])
        self.accept("CharacterCollisions-out-Speek_PlantHere", self.hideText)
        self.accept("CharacterCollisions-in-Speek_GoAway", self.goAway1)
        self.accept("CharacterCollisions-out-Speek_GoAway", self.hideText)
        self.accept("CharacterCollisions-in-Speek_SoTired", self.showText, extraArgs=[_("I'm tired, I planted to many seeds.")])
        self.accept("CharacterCollisions-out-Speek_SoTired", self.hideText)
        self.accept("CharacterCollisions-in-Speek_Fungies", self.showText, extraArgs=[_("Fungi 1: I hope such a fire never comes again\nFungi 2: Me too\nFungi 3: Do you smell the smoke o.O")])
        self.accept("CharacterCollisions-out-Speek_Fungies", self.hideText)
        self.accept("CharacterCollisions-in-Speek_MysteriousVoice", self.showText, extraArgs=[_("Voice from above: Hey you there, little droplet, it's me, the creator.\nYou: are you god?\nVoice from above: No, just the developer :P...")])
        self.accept("CharacterCollisions-out-Speek_MysteriousVoice", self.hideText)
        self.accept("CharacterCollisions-in-Speek_LonelyRock", self.findTheLonlyRock)
        self.accept("CharacterCollisions-out-Speek_LonelyRock", self.hideText)




        self.accept("Bridge1_Built", self.changeSpeaker1)

        # other events
        self.accept("player-plant_seed", self.doPlantSeed)
        self.accept("f1", self.showTutorial, extraArgs=[None])
        self.accept("addPoints", self.addPoints)
        self.accept("drawPlayerWater", self.drawPlayerWater)

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
        self.outroSequence.finish()
        self.tutorial1.removeNode()
        self.intro1.removeNode()
        self.intro2.removeNode()
        self.intro3.removeNode()
        self.outro1.removeNode()
        self.outro2.removeNode()
        self.outro3.removeNode()
        self.tut1.removeNode()
        self.tut2.removeNode()
        self.gameOver1.removeNode()
        self.hud.cleanup()

    def finishGame(self, args):
        self.request("Outro")

    def requestEscape(self):
        if self.state == "Intro":
            self.request("Main")
            return False
        else:
            return True

    def showTutorial(self, args):
        if not self.tutorialInterval.isPlaying():
            self.tutorialInterval.start()

    def showText(self, text, args):
        self.hud.showSpeekText(text)

    def hideText(self, args):
        self.hud.hideSpeekText()

    def goAway1(self, args):
        self.hud.showSpeekText(_("I'm just standing here, go away..."))
        self.ignore("CharacterCollisions-in-Speek_GoAway")
        self.accept("CharacterCollisions-in-Speek_GoAway", self.goAway2)

    def goAway2(self, args):
        self.hud.showSpeekText(_("Go away, please..."))
        self.ignore("CharacterCollisions-in-Speek_GoAway")
        self.accept("CharacterCollisions-in-Speek_GoAway", self.goAway3)

    def goAway3(self, args):
        self.hud.showSpeekText(_("Take some of my water but now go away, please..."))
        self.water += 20
        self.points += 10
        self.hud.setWater(self.water)
        self.hud.setPoints(self.points)
        newScale = self.water/100.0
        self.player.setScale(newScale)
        self.ignore("CharacterCollisions-in-Speek_GoAway")
        self.accept("CharacterCollisions-in-Speek_GoAway", self.goAway4)

    def goAway4(self, args):
        self.hud.showSpeekText(_("..."))

    def findTheLonlyRock(self, args):
        self.points += 50
        self.hud.setPoints(self.points)
        self.hud.showSpeekText(_("Lonely Rock: No one ever talks to me ;(\nYou: Poor little rock *pat pat*"))
        self.accept("CharacterCollisions-in-Speek_LonelyRock", self.showText, extraArgs=[_("Lonely Rock: No one ever talks to me ;(\nYou: Poor little rock *pat pat*")])

    def theFriendlyDroplet(self, args):
        self.hud.showSpeekText(_("Up here are no seeds, but take some of this water!"))
        self.water += 10
        self.points += 10
        self.hud.setWater(self.water)
        self.hud.setPoints(self.points)
        newScale = self.water/100.0
        self.player.setScale(newScale)
        self.accept("CharacterCollisions-in-Speek_NoSeeds", self.showText, extraArgs=[_("Up here are no seeds...")])

    def changeSpeaker1(self):
        self.ignore("CharacterCollisions-in-Speek_PlantHere")
        self.accept("CharacterCollisions-in-Speek_PlantHere", self.showText, extraArgs=[_("Awesome!")])

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

    def doPlantSeed(self):
        self.level.doPlantSeed(self.currentPlantingGround)

    def addPoints(self, points):
        self.points += points
        self.hud.setPoints(self.points)

    def drawPlayerWater(self, amount):
        self.water -= amount
        self.hud.setWater(self.water)
        newScale = self.water/100.0
        if self.water == 0:
            self.player.hide()
            self.request("GameOver")
            return
        self.player.setScale(newScale)

    def setEndingStoryText(self):
        self.hud.setStory(_("You got %d soul points") % self.points)

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

    def enterOutro(self):
        startPoint = self.level.getEndPoint()
        if startPoint is not None:
            self.player.setStartPos(startPoint.getPos())
            self.player.setStartHpr(startPoint.getHpr())
        self.player.centerCamera()
        self.outroSequence.start()

    def exitOutro(self):
        self.outroSequence.finish()

    def enterGameOver(self):
        self.gameOverSequence.start()

    def exitGameOver(self):
        self.gameOverSequence.finish()
