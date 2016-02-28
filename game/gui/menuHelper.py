#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PANDA3D ENGINE IMPORTS
#
from direct.gui.DirectGui import DirectButton
from panda3d.core import TextNode

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


def createButton(text, btnGeom, xPos, yPos, args):
    buttonSize = (-1.15, 1.15, 0.50, -0.25)
    btn = DirectButton(
        scale=0.25,
        # some temp text
        text=text,
        text_scale=0.5,
        # set the alignment to right
        text_align=TextNode.ACenter,
        # set the text color to black
        text_fg=(0, 0, 0, 1),
        # set the buttons images
        relief=1,
        frameColor=(0,0,1,1),
        frameSize=buttonSize,
        pressEffect=False,
        pos=(xPos, 0, yPos),
        command=base.messenger.send,
        extraArgs=args,
        rolloverSound=None,
        clickSound=None)
    # check if the text is to long and resize the frame if necessary
    if btn.getBounds()[0] < buttonSize[0] or \
            btn.getBounds()[1] > buttonSize[1]:
        btn["frameSize"] = (
            btn.getBounds()[0]-0.2, btn.getBounds()[1]+0.2,
            buttonSize[2], buttonSize[3])
        btn.resetFrameSize()
    btn.setTransparency(True)
    return btn
