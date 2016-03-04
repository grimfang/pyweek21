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
    ColorBlendAttrib,
    Fog,)

from panda3d.core import Plane, PlaneNode, TransparencyAttrib, Texture, Vec3, Point3, NodePath, TextureStage, CullFaceAttrib, BitMask32
from direct.actor.Actor import Actor

# Game imports
from seed.seed import Seed

__author__ = "MJ-meo-dmt & Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Level():
    def __init__(self, player):
        self.player = player

        loader.loadModel("skybox/Skybox", callback=self.skyBoxDone)

        # Visual model "Ground"
        loader.loadModel("forest/Forest", callback=self.levelDone)

    def skyBoxDone(self, model):
        self.skybox = model
        self.skybox.setScale(0.8)
        self.skybox.setPos(0, 0, 0.5)
        self.skybox.setDepthTest(False)
        self.skybox.setAttrib(CullBinAttrib.make("skyboxBin", 1000))
        self.skybox.reparentTo(camera)
        taskMgr.add(self.skyboxTask, "forestsky")

    def levelDone(self, model):
        self.level = model
        self.level.hide()
        self.level.reparentTo(render)
        self.level.setPos(0, 0, -2)

    	# lights for this world
    	directLight = DirectionalLight("directLight")
    	directLightNP = self.level.attachNewNode(directLight)
    	directLightNP.setHpr(0, -60, 0)
    	render.setLight(directLightNP)

        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(VBase4(0.2, 0.2, 0.2, 1))
        ambientLightNP = self.level.attachNewNode(ambientLight)
        render.setLight(ambientLightNP)

        # spawn NPCs
        self.numNPCs = 15
        self.npcList = []
        for i in range(self.numNPCs):
            npc = Actor(
                "character/character",
                {"Idle": "character/character-Idle"})
            npc.setBlend(frameBlend=True)
            npc.setScale(random.uniform(0.4, 1.0))
            npc.loop("Idle")
            point = self.level.find("**/NPC.%03d"%i)
            npc.reparentTo(point)
            self.npcList.append(npc)

        #
        # Fix alpha problems
        #
        alphaSettings = ColorBlendAttrib.make(
            ColorBlendAttrib.MAdd,
            ColorBlendAttrib.OIncomingAlpha,
            ColorBlendAttrib.OOne,
            (0, 0, 0, 0))
        for np in self.level.findAllMatches("**/Godray*"):
            np.setAttrib(alphaSettings)
            np.setBin("fixed", 10)
            np.setDepthWrite(False)
        water = self.level.find("**/Water")
        water.setAttrib(alphaSettings)
        water.setBin("fixed", 11)
        water.setDepthWrite(False)

        # Extra Collision solids
        loader.loadModel("forest/Bridge1", callback=self.bridge1Done)
        loader.loadModel("forest/Bridge2", callback=self.bridge2Done)
        loader.loadModel("forest/Bridge3", callback=self.bridge3Done)
        loader.loadModel("forest/Bridge4", callback=self.bridge4Done)
        loader.loadModel("forest/Plant1", callback=self.plant1Done)
        loader.loadModel("forest/Plant2", callback=self.plant2Done)

        # some light green fog
        self.fog = Fog("Forest Fog")
        self.fog.setColor(0.0, 0.9, 0.7)
        self.fog.setExpDensity(0.01)
        render.setFog(self.fog)

        ## Seeds ##
        self.numSeedPositions = 20
        self.tutorialSeed = None
        self.spawnedSeeds = {}

        self.spawnSeeds(15)

        base.messenger.send("LevelLoaded")

    def bridge1Done(self, model):
        self.bridge1 = model

    def bridge2Done(self, model):
        self.bridge2 = model

    def bridge3Done(self, model):
        self.bridge3 = model

    def bridge4Done(self, model):
        self.bridge4 = model

    def plant1Done(self, model):
        self.plant1 = model

    def plant2Done(self, model):
        self.plant2 = model

    def stop(self):
        self.clearSeeds()
        self.level.clearLight()
        self.level.removeNode()
        render.clearLight()
        render.clearFog()
        taskMgr.remove("forestsky")
        self.skybox.removeNode()
        for npc in self.npcList:
            npc.cleanup()
            npc.removeNode()
        self.npcList = None

    def show(self):
        self.level.show()

    def hide(self):
        self.level.hide()

    def clearSeeds(self):
        for seed in self.spawnedSeeds.values():
            seed.Destroy()

        self.tutorialSeed.Destroy()
        self.seedSpawnPositions = []
        self.spawnedSeeds = {}

    def getStartPoint(self):
        startPosNode = self.level.find("**/StartPos")
        if startPosNode:
            return startPosNode
        return None

    def getEndPoint(self):
        endPosNode = self.level.find("**/EndPos")
        if endPosNode:
            return endPosNode
        return None

    def skyboxTask(self, task):
        self.skybox.setHpr(render, 0, 0, 0)
        return task.cont

    def spawnSeeds(self, numOfSeeds):
        self.seedSpawnPositions = self.getSeedSpawnPoints()

        self.usedPositions = []

        for idx in range(numOfSeeds):

            if idx == 0:
                spawnPos = self.seedSpawnPositions[0]
                self.spawnedSeeds[spawnPos.getName()] = Seed()
                self.spawnedSeeds[spawnPos.getName()].OnSpawn(spawnPos)#.getPos(), self.level)
                self.tutorialSeed = self.spawnedSeeds[spawnPos.getName()]

            else:
                randPos = random.randint(1, len(self.seedSpawnPositions)-1)
                if randPos in self.usedPositions:
                    while randPos in self.usedPositions:
                        randPos = random.randint(1, len(self.seedSpawnPositions)-1)
                self.usedPositions.append(randPos)

                spawnPos = self.seedSpawnPositions[randPos]
                self.spawnedSeeds[spawnPos.getName()] = Seed()
                self.spawnedSeeds[spawnPos.getName()].OnSpawn(spawnPos)#.getPos(), self.level)

    def getSeedSpawnPoints(self):
        points = []
        for idx in range(self.numSeedPositions):
            points.append(self.level.find("**/SeedPos.%03d"%idx))

        return points

    def doPickupSeed(self, args):
        if self.player.carry_seed == True:
            return
        self.player.carry_seed = True
        seedName = args.getIntoNode().getName()
        for seed in self.spawnedSeeds:
            cid = "seedSphere-" + self.spawnedSeeds[seed].id
            if cid == seedName: # and self.spawnedSeeds[seed].seedState == 0:
                self.spawnedSeeds[seed].DoPickup(self.player)

    def doPlantSeed(self, plantGround):
        if self.player.carry_seed == False:
            return
        self.player.carry_seed = False
        for seed in self.spawnedSeeds:
            if self.spawnedSeeds[seed].seedState == 1:
                self.spawnedSeeds[seed].DoPlantSeed(plantGround.getIntoNodePath().getParent())

                playerPlantPoint = plantGround.getIntoNodePath().getParent().find("**/PlayerPlantingPos")

                self.player.setStartHpr(playerPlantPoint.getHpr(render))
                self.player.setStartPos(playerPlantPoint.getPos(render))

                plantGroundNP = plantGround.getIntoNodePath().getParent().getParent()
                plantGroundName = plantGroundNP.getName()
                base.cTrav.removeCollider(plantGround.getIntoNodePath())
                if plantGroundName == "PlantGround.000":
                    #Bridge 1
                    def buildBridge1(task):
                        plantGroundNP.removeNode()
                        self.bridge1.reparentTo(self.level)
                    base.messenger.send("Bridge1_Built")
                    base.messenger.send("addPoints", [200])
                    base.messenger.send("drawPlayerWater", [10])
                    taskMgr.doMethodLater(3.0, buildBridge1, "Build 1st Bridge")
                elif plantGroundName == "PlantGround.001":
                    #Bridge 2
                    def buildBridge2(task):
                        plantGroundNP.removeNode()
                        self.bridge2.reparentTo(self.level)
                    base.messenger.send("addPoints", [300])
                    base.messenger.send("drawPlayerWater", [10])
                    taskMgr.doMethodLater(3.0, buildBridge2, "Build 2nd Bridge")
                elif plantGroundName == "PlantGround.002":
                    #Bridge 3
                    def buildBridge3(task):
                        plantGroundNP.removeNode()
                        self.bridge3.reparentTo(self.level)
                    base.messenger.send("addPoints", [400])
                    base.messenger.send("drawPlayerWater", [15])
                    taskMgr.doMethodLater(3.0, buildBridge3, "Build 3rd Bridge")
                elif plantGroundName == "PlantGround.003":
                    #Bridge 4
                    def buildBridge4(task):
                        plantGroundNP.removeNode()
                        self.bridge4.reparentTo(self.level)
                    base.messenger.send("addPoints", [500])
                    base.messenger.send("drawPlayerWater", [20])
                    taskMgr.doMethodLater(3.0, buildBridge4, "Build 4th Bridge")
                else:
                    def growPlant(task):
                        if random.choice([True, False]):
                            self.plant1.setPos(plantGroundNP.getPos(render))
                            self.plant1.setZ(self.plant1, 2)
                            self.plant1.setH(random.uniform(0.0, 360.0))
                            self.plant1.copyTo(self.level)
                        else:
                            self.plant2.setPos(plantGroundNP.getPos(render))
                            self.plant2.setZ(self.plant2, 2)
                            self.plant2.setH(random.uniform(0.0, 360.0))
                            self.plant2.copyTo(self.level)
                        plantGroundNP.removeNode()
                    base.messenger.send("addPoints", [100])
                    base.messenger.send("drawPlayerWater", [5])
                    taskMgr.doMethodLater(5, growPlant, "Grow normal plant")
                    plantGround.getIntoNodePath().removeNode()
                break
