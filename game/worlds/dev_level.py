#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from panda3d.core import DirectionalLight

# Game imports

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class DevLevel():
    def __init__(self):
        
    	# lights for this world
    	directLight = DirectionalLight("directLight")
    	directLightNP = render.attachNewNode(directLight)
    	directLightNP.setHpr(0, -60, 0)
    	render.setLight(directLightNP)

        # Visual model "Ground"
        self.devLevel = loader.loadModel("./assets/devLevel")
        self.devLevel.reparentTo(render)

        self.devLevel.setPos(0, 30, 0)