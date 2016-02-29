#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PYTHON IMPORTS
#
import os

#
# PANDA3D ENGINE IMPORTS
#
from direct.gui.DirectGui import (
    DirectFrame,
    DirectSlider,
    DirectLabel)
from direct.gui.DirectCheckBox import DirectCheckBox
from panda3d.core import TextNode

#
# GAME IMPORTS
#
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

        self.btnBack = menuHelper.createButton(_("Back"), btnGeom, 0, -0.7, ["options_back"])
        self.btnBack.reparentTo(self.frameMain)


        volume = base.musicManager.getVolume()
        self.sliderVolume = DirectSlider(
            scale=0.5,
            pos=(-0.5, 0, 0),
            range=(0, 1),
            scrollSize=0.01,
            text=_("Volume %d%%") % volume*100,
            text_scale=0.1,
            text_pos=(0, 0.15),
            text_fg=(1, 1, 1, 1),
            thumb_frameColor=(0,0.75, 0.25, 1),
            frameColor=(0.35, 0.15, 0.05, 1),
            value=volume,
            command=self.sliderVolume_ValueChanged)
        self.sliderVolume.reparentTo(self.frameMain)

        isChecked = not base.AppHasAudioFocus
        img = None
        imgON = "gui/AudioSwitch_on.png"
        imgOFF = "gui/AudioSwitch_off.png"
        if base.AppHasAudioFocus:
            img = imgON
        else:
            img = imgOFF
        self.cbVolumeMute = DirectCheckBox(
            text=_("Mute Audio"),
            text_scale=0.5,
            text_align=TextNode.ACenter,
            text_pos=(0, 0.65),
            text_fg=(1, 1, 1, 1),
            scale=0.105,
            pos=(0.5, 0, 0),
            command=self.cbVolumeMute_CheckedChanged,
            relief=None,
            pressEffect=False,
            isChecked=isChecked,
            image=img,
            image_scale=0.5,
            checkedImage=imgOFF,
            uncheckedImage=imgON)
        self.cbVolumeMute.setTransparency(True)
        self.cbVolumeMute.setImage()
        self.cbVolumeMute.reparentTo(self.frameMain)

        prcPath = os.path.join(basedir, "%s.prc"%appName)
        self.advancedOptions = DirectLabel(
            text=_("Advanced options can be made in the following text file\n%s")%prcPath,
            text_scale=0.5,
            text_fg=(1, 1, 1, 1),
            scale=0.1,
            pos=(0, 0, -0.25),
            frameColor=(0, 0, 0, 0))
        self.advancedOptions.setTransparency(True)
        self.advancedOptions.reparentTo(self.frameMain)

        self.hide()

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()

    def cbVolumeMute_CheckedChanged(self, checked):
        if checked:
            base.disableAllAudio()
        else:
            base.enableAllAudio()

    def sliderVolume_ValueChanged(self):
        volume = round(self.sliderVolume["value"], 2)
        self.sliderVolume["text"] = _("Volume %d%%") % int(volume * 100)
        base.sfxManagerList[0].setVolume(volume)
        base.musicManager.setVolume(volume)
