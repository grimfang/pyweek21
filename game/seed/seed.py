#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts
from panda3d.core import CollisionSphere, CollisionNode

# Game imports

__author__ = "MJ-meo-dmt"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Seed():
    def __init__(self):

    	self.id = 'seed'
    	self.seed = None

    def OnSpawn(self, pos):
    	# Spawn in world (default)

    	# Load a model for now its just one.
    	self.seed = loader.loadModel("./assets/seed/seed")
    	self.SetParent(render)
    	self.seed.setPos(pos)

    	# Collision body
    	cs = CollisionSphere(0, 0, 0, 0.3)
    	cnodePath = self.seed.attachNewNode(CollisionNode('collisionSphere'))
    	cnodePath.node().addSolid(cs)

    	cnodePath.show()

    def OnPickup(self):
    	# When the player touches the object "seed"
    	pass

    def SetParent(self, newParent):
    	if self.seed != None:
    		self.seed.reparentTo(newParent)
    	else:
    		print "No seed object spawned"

    def Destroy(self):
    	self.seed.removeNode()