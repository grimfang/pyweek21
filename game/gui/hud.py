#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PANDA3D ENGINE IMPORTS
#
from direct.gui.DirectLabel import DirectLabel
from panda3d.core import TextNode


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

    def cleanup(self):
        self.canPlantLabel.destroy()
        self.points.destroy()
        self.playerWater.destroy()
        self.helpInfo.destroy()

    def showCanPlant(self):
        self.canPlantLabel.show()

    def hideCanPlant(self):
        self.canPlantLabel.hide()

    def setPoints(self, points):
        self.points["test"] = _("Points: %d")%points

    def setWater(self, water):
        self.playerWater["test"] = _("Remaining Water: %d")%water
