#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from panda3d.core import CollisionSphere, CollisionNode, BitMask32

# Game imports

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Seed():
    def __init__(self):
        self.id = "seed" + str(id(self))
        self.seed = None
        self.cnodePath = None

        # Spawned = 0
        # PickedUp = 1
        # Planeted = 2
        # Growing = 3
        self.seedState = None

    def OnSpawn(self, parent):
        # Spawn in world (default)

        # Load a model for now its just one.
        self.seed = loader.loadModel("./assets/seed/seed")
        self.seedNP = self.seed.reparentTo(parent)
        self.seed.setZ(1)

        # Collision body
        cs = CollisionSphere(0, 0, 0, 0.4)
        cs.setTangible(False)
        self.cnodePath = self.seed.attachNewNode(CollisionNode("seedSphere-" + self.id))
        self.cnodePath.node().addSolid(cs)
        self.cnodePath.node().setIntoCollideMask(BitMask32(0x80))  # 1000 0000

        #self.cnodePath.show()

        self.seedState = 0

    def DoPlantSeed(self, plantingGround):
        npos = (0, 0, 0)
        self.seed.setHpr(0, 0, 90)
        self.seedNP = self.seed.reparentTo(plantingGround)
        self.seed.setPos(npos)
        self.OnPlanted()

    def OnPlanted(self):
        # Start growing timer /check /things
        self.seedState = 2

    def DoPickup(self, player):
        # When the player touches the object "seed"
        self.seedState = 1
        self.RemoveCollisionNode()
        self.seedNP = self.seed.reparentTo(player.mainNode)
        self.seed.setPos(0, 0, player.player_height+0.2)

    def RemoveCollisionNode(self):
        if self.cnodePath != None:
            base.cTrav.removeCollider(self.cnodePath)
            self.cnodePath.removeNode()

    def Destroy(self):
        self.RemoveCollisionNode()
        self.seed.removeNode()
