#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from direct.showbase.DirectObject import DirectObject

# Game imports
from core import helper

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Player(DirectObject):
    def __init__(self):
        
        self.player = loader.loadModel("./assets/player")
        self.player.reparentTo(render)
        

