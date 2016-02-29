#!/usr/bin/python
# -*- coding: utf-8 -*-

# Panda3D imoprts

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
    	self.OnSpawn()


    def OnSpawn(self):
    	# Spawn in world (default)

    	# Load a model for now its just one.
    	self.seed = loader.loadModel("./assets/seed/seed")
    	self.SetParent(render)

    def OnPickup(self):
    	# When the player touches the object "seed"
    	pass

    def SetParent(self, newParent):
    	if self.seed != None:
    		self.seed.reparentTo(newParent)
    	else:
    		print "No seed object spawned"