#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PANDA3D ENGINE IMPORTS
#
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode, BillboardEffect


class HUD():
    def __init__(self):
        self.canPlantLabel = DirectLabel(
            frameColor=(0, 0, 0, 0.25),
            text_fg=(1, 1, 1, 1),
            scale=0.15,
            pos=(0, 0, 0.25),
            pad=(0.2,0.2),
            text=_("Plant Seed"))
        self.canPlantLabel.setTransparency(True)
        self.canPlantLabel.reparentTo(base.a2dBottomCenter)
        self.canPlantLabel.hide()

        self.speekLabel = DirectLabel(
            frameColor=(0, 0, 0, 0.25),
            text_fg=(1, 1, 1, 1),
            scale=0.15,
            pos=(0, 0, 0.5),
            pad=(0.2,0.2),
            text="...")
        self.speekLabel.reparentTo(render)
        self.speekLabel.hide()
        self.speekLabel.setTransparency(True)
        self.speekLabel.setEffect(BillboardEffect.makePointEye())
        self.speekLabel.setBin("fixed", 11)
        self.speekLabel.setDepthWrite(False)

        self.storyText = DirectLabel(
            frameColor=(0, 0, 0, 0.25),
            text_fg=(1, 1, 1, 1),
            scale=0.08,
            pos=(0, 0, 0.25),
            pad=(0.2,0.2),
            text="Story text")
        self.storyText.setTransparency(True)
        self.storyText.reparentTo(base.a2dBottomCenter)
        self.storyText.hide()

        self.points = DirectLabel(
            frameColor=(0, 0, 0, 0.25),
            text_fg=(1, 1, 1, 1),
            scale=0.075,
            pos=(0.05, 0, -0.1),
            pad=(0.2,0.2),
            text_align=TextNode.ALeft,
            text=_("Points: %d")%0)
        self.points.setTransparency(True)
        self.points.reparentTo(base.a2dTopLeft)

        self.playerWater = DirectLabel(
            frameColor=(0, 0, 0, 0.25),
            text_fg=(1, 1, 1, 1),
            scale=0.075,
            pos=(0.05, 0, -0.2),
            pad=(0.2,0.2),
            text_align=TextNode.ALeft,
            text=_("Remaining Water: %d")%100)
        self.playerWater.setTransparency(True)
        self.playerWater.reparentTo(base.a2dTopLeft)


        self.helpInfo = DirectLabel(
            frameColor=(0, 0, 0, 0.25),
            text_fg=(1, 1, 1, 1),
            scale=0.075,
            pos=(-0.05, 0, -0.1),
            pad=(0.2,0.2),
            text_align=TextNode.ARight,
            text=_("F1 - show help"))
        self.helpInfo.setTransparency(True)
        self.helpInfo.reparentTo(base.a2dTopRight)

        self.hide()

    def show(self):
        self.points.show()
        self.playerWater.show()
        self.helpInfo.show()

    def hide(self):
        self.points.hide()
        self.playerWater.hide()
        self.helpInfo.hide()

    def hideAll(self):
        self.canPlantLabel.hide()
        self.speekLabel.hide()
        self.points.hide()
        self.playerWater.hide()
        self.helpInfo.hide()

    def showStory(self):
        self.storyText.show()

    def hideStory(self):
        self.storyText.hide()

    def cleanup(self):
        self.hideAll()
        self.canPlantLabel.destroy()
        self.speekLabel.destroy()
        self.points.destroy()
        self.playerWater.destroy()
        self.helpInfo.destroy()

    def showCanPlant(self):
        self.canPlantLabel.show()

    def hideCanPlant(self):
        self.canPlantLabel.hide()

    def setPoints(self, points):
        self.points["text"] = _("Points: %d")%points
        self.points.resetFrameSize()

    def setWater(self, water):
        self.playerWater["text"] = _("Remaining Water: %d")%water
        self.playerWater.resetFrameSize()

    def setStory(self, storytext):
        self.storyText["text"] = storytext
        self.storyText.resetFrameSize()

    def showSpeekText(self, text, newPos):
        self.speekLabel.setPos(newPos)
        self.speekLabel["text"] = text
        self.speekLabel.resetFrameSize()
        self.speekLabel.show()

    def hideSpeekText(self):
        self.speekLabel.hide()

