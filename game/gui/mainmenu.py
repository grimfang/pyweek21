#!/usr/bin/python
# -*- coding: utf-8 -*-

from direct.gui.DirectGui import DirectFrame
import menuHelper

class Mainmenu():
    def __init__(self):
        self.frameMain = DirectFrame(
            image="gui/MenuBackground.png",
            image_scale=(1.7778, 1, 1),
            #image_pos=(0, 0, 0.25),
            frameSize=(
                base.a2dLeft, base.a2dRight,
                base.a2dTop, base.a2dBottom),
            frameColor=(0,0,0,0))
        self.frameMain.setTransparency(True)

        self.logo = DirectFrame(
            image="Logo.png",
            image_scale=0.45,
            image_pos=(0, 0, 0.35),
            frameSize=(
                base.a2dLeft, base.a2dRight,
                base.a2dTop, base.a2dBottom),
            frameColor=(0,0,0,0))
        self.logo.reparentTo(self.frameMain)

        btnGeom = "gui/button"

        self.btnStart = menuHelper.createButton(_("Start"), btnGeom, 0, -0.7, ["menu_start"])
        self.btnStart.reparentTo(self.frameMain)

        self.btnOptions = menuHelper.createButton(_("Options"), btnGeom, -1.0, -0.7, ["menu_options"])
        self.btnOptions.reparentTo(self.frameMain)

        self.btnQuit = menuHelper.createButton(_("Quit"), btnGeom, 1.0, -0.7, ["menu_quit"])
        self.btnQuit.reparentTo(self.frameMain)

        self.hide()

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()
