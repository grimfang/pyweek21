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

    def OnSpawn(self, pos):
    	# Spawn in world (default)

    	# Load a model for now its just one.
    	self.seed = loader.loadModel("./assets/seed/seed")
    	self.SetParent(render)
    	posn = (pos.x, pos.y, pos.z-1)
    	self.seed.setPos(posn)

    	# Collision body
    	cs = CollisionSphere(0, 0, 0, 0.4)
        cs.setTangible(False)
    	self.cnodePath = self.seed.attachNewNode(CollisionNode("seedSphere-" + self.id))
    	self.cnodePath.node().addSolid(cs)
        self.cnodePath.node().setIntoCollideMask(BitMask32(0x80))  # 1000 0000

    	self.cnodePath.show()

        self.seedState = 0

    def DoPlantSeed(self, newPos):
        self.SetParent(render)
        self.seed.setPos(newPos)
        self.OnPlanted()

    def OnPlanted(self):
        # Start growing timer /check /things
        self.seedState = 2
        print "SEED PLANTED, START GROWING!!"

    def DoPickup(self, player):
    	# When the player touches the object "seed"
        print "PICKUP SEED"
        self.RemoveCollisionNode()
        self.SetParent(player.mainNode)
        self.seed.setPos(0, 0, player.player_height+0.2)

        self.seedState = 1

    def SetParent(self, newParent):
    	if self.seed != None:
    		self.seed.reparentTo(newParent)
    	else:
    		print "No seed object spawned"

    def RemoveCollisionNode(self):
        if self.cnodePath != None:
            base.cTrav.removeCollider(self.cnodePath)
            self.cnodePath.hide()

    def Destroy(self):
        print "destroy seed"
    	self.seed.removeNode()
        self.cnodePath = None
