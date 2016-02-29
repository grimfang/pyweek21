#!/usr/bin/python
# -*- coding: utf-8 -*-

from direct.gui.DirectGui import DirectFrame
import menuHelper

class Optionsmenu():
    def __init__(self):
        self.frameMain = DirectFrame(
            image="Logo.png",
            image_scale=0.25,
            image_pos=(0, 0, 0.55),
            frameSize=(
                base.a2dLeft, base.a2dRight,
                base.a2dTop, base.a2dBottom),
            frameColor=(0,0,0,0))
        self.frameMain.setTransparency(True)

        btnGeom = "gui/button"

        self.btnStart = menuHelper.createButton(_("Back"), btnGeom, 0, -0.7, ["options_back"])
        self.btnStart.reparentTo(self.frameMain)

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()
