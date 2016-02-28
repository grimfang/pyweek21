#!/usr/bin/python
# -*- coding: utf-8 -*-

from direct.gui.DirectGui import DirectFrame
import menuHelper

class Mainmenu():
    def __init__(self):
        self.frameMain = DirectFrame(
            frameSize=(
                base.a2dLeft, base.a2dRight,
                base.a2dTop, base.a2dBottom),
            frameColor=(0,1,0,1))
        self.frameMain.setTransparency(True)

        #TODO: Load the buttons geometry
        btnGeom = None

        self.btnStart = menuHelper.createButton(_("Start"), btnGeom, 0, 0.5, ["menu_start"])
        self.btnStart.reparentTo(self.frameMain)

        self.btnOptions = menuHelper.createButton(_("Options"), btnGeom, 0.0, 0.0, ["menu_options"])
        self.btnOptions.reparentTo(self.frameMain)

        self.btnQuit = menuHelper.createButton(_("Quit"), btnGeom, 0.0, -0.5, ["menu_quit"])
        self.btnQuit.reparentTo(self.frameMain)

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()
