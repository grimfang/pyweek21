#!/usr/bin/python
# -*- coding: utf-8 -*-
# Python Import
import random

# Panda3D imoprts
from panda3d.core import (
    DirectionalLight,
    AmbientLight,
    VBase4,
    CullBinAttrib,
    Fog,)

from panda3d.core import Plane, PlaneNode, TransparencyAttrib, Texture, Vec3, Point3, NodePath, TextureStage, CullFaceAttrib, BitMask32

# Game imports
from seed.seed import Seed

__author__ = "MJ-meo-dmt & Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Level():
    def __init__(self):
        self.skybox = loader.loadModel("skybox/Skybox")
        self.skybox.setScale(0.8)
        self.skybox.setPos(0, 0, 0.5)
        self.skybox.setDepthTest(False)
        self.skybox.setAttrib(CullBinAttrib.make("skyboxBin", 1000))
        self.skybox.reparentTo(camera)
        taskMgr.add(self.skyboxTask, "forestsky")

        # Visual model "Ground"
        self.level = loader.loadModel("forest/Forest")
        self.level.reparentTo(render)

        # some light green fog
        self.fog = Fog("Forest Fog")
        self.fog.setColor(0.0, 0.9, 0.7)
        self.fog.setExpDensity(0.01)
        self.skybox.setFog(self.fog)
        render.setFog(self.fog)

    	# lights for this world
    	directLight = DirectionalLight("directLight")
    	directLightNP = self.level.attachNewNode(directLight)
    	directLightNP.setHpr(0, -60, 0)
    	render.setLight(directLightNP)

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        ambientLightNP = self.level.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)

        self.level.setPos(0, 0, -2)

        ## Seeds ##
        self.numSeedPositions = 20
        self.tutorialSeed = None
        self.spawnedSeeds = {}

        self.spawnSeeds(7)


    def stop(self):
        self.clearSeeds()
        self.level.clearLight()
        self.level.removeNode()
        render.clearLight()
        render.clearFog()
        taskMgr.remove("forestsky")
        self.skybox.removeNode()

    def clearSeeds(self):
        # Fireclaw just check these and make nicer if needed
        for seed in self.spawnedSeeds:
            self.spawnedSeeds[seed].Destroy()

        self.tutorialSeed.Destroy()
        self.seedSpawnPositions = []
        self.spawnedSeeds = {}

    def getStartPoint(self):
        startPosNode = self.level.find("**/StartPos")
        if startPosNode:
            return startPosNode
        return None

    def skyboxTask(self, task):
        self.skybox.setHpr(render, 0, 0, 0)
        return task.cont

    def spawnSeeds(self, numOfSeeds):
        self.seedSpawnPositions = self.getSeedSpawnPoints()

        for idx in range(numOfSeeds):

            if idx == 0:
                spawnPos = self.seedSpawnPositions[0]
                self.spawnedSeeds[spawnPos.getName()] = Seed()
                self.spawnedSeeds[spawnPos.getName()].OnSpawn(spawnPos.getPos())
                self.tutorialSeed = self.spawnedSeeds[spawnPos.getName()]

            else:
                randPos = random.randint(1, len(self.seedSpawnPositions)-1)

                spawnPos = self.seedSpawnPositions[randPos]
                self.spawnedSeeds[spawnPos.getName()] = Seed()
                self.spawnedSeeds[spawnPos.getName()].OnSpawn(spawnPos.getPos())


    def getSeedSpawnPoints(self):
        points = []
        for idx in range(self.numSeedPositions):
            points.append(self.level.find("**/SeedPos.%03d"%idx))

        return points


