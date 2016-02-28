#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from panda3d.core import (
    DirectionalLight,
    AmbientLight,
    VBase4,
    CullBinAttrib,
    Fog,)

# Game imports

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class DevLevel():
    def __init__(self):
        self.skybox = loader.loadModel("skybox/Skybox")
        self.skybox.setScale(0.8)
        self.skybox.setPos(0, 0, 0.5)
        self.skybox.setDepthTest(False)
        self.skybox.setAttrib(CullBinAttrib.make("skyboxBin", 1000))
        self.skybox.reparentTo(camera)
        taskMgr.add(self.skyboxTask, "forestsky")

        self.fog = Fog("Forest Fog")
        self.fog.setColor(0.0, 0.9, 0.7)
        self.fog.setExpDensity(0.01)
        self.skybox.setFog(self.fog)
        render.setFog(self.fog)

    	# lights for this world
    	directLight = DirectionalLight("directLight")
    	directLightNP = render.attachNewNode(directLight)
    	directLightNP.setHpr(0, -60, 0)
    	render.setLight(directLightNP)


        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        ambientLightNP = render.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)

        # Visual model "Ground"
        #self.devLevel = loader.loadModel("devLevel")
        self.devLevel = loader.loadModel("forest/Forest")
        self.devLevel.reparentTo(render)

        self.devLevel.setPos(0, 0, -2)

    def skyboxTask(self, task):
        self.skybox.setHpr(render, 0, 0, 0)
        return task.cont
