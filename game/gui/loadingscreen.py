#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PANDA3D ENGINE IMPORTS
#
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel)
from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TextNode

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


class LoadingScreen():
    """Show a directWaitbar to display the current loading state of the
    application"""
    def __init__(self):
        # a fill panel so the player doesn't see how everything
        # gets loaded in the background
        self.frameMain = DirectFrame(
            image="gui/MenuBackground.png",
            image_scale=(1.7778, 1, 1),
            #image_pos=(0, 0, 0.25),
            frameSize=(
                base.a2dLeft, base.a2dRight,
                base.a2dTop, base.a2dBottom),
            frameColor=(0,0,0,0))
        self.frameMain.setTransparency(True)
        self.frameMain.setBin("fixed", 6000)
        self.frameMain.setDepthWrite(False)

        self.logo = DirectFrame(
            image="Logo.png",
            image_scale=0.25,
            image_pos=(0, 0, 0.55),
            frameSize=(
                base.a2dLeft, base.a2dRight,
                base.a2dTop, base.a2dBottom),
            frameColor=(0,0,0,0))
        self.logo.reparentTo(self.frameMain)


        # the text Loading...
        self.lblLoading = DirectLabel(
            scale=0.10,
            pos=(0, 0, -0.15),
            frameColor=(0, 0, 0, 0),
            text=_("Loading..."),
            text_align=TextNode.ACenter,
            text_fg=(1, 1, 1, 1))
        self.lblLoading.reparentTo(self.frameMain)

        self.stop()

    def start(self):
        self.frameMain.show()
        base.graphicsEngine.renderFrame()
        base.graphicsEngine.renderFrame()

    def stop(self):
        self.frameMain.hide()
