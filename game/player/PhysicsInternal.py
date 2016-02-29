#!/usr/bin/python
# -*- coding: utf-8 -*-

from panda3d.core import (
    CollisionTraverser,
    CollisionHandlerQueue,
    CollisionHandlerPusher,
    CollisionHandlerFloor,
    CollisionNode,
    CollisionSphere,
    CollisionSegment,
    CollisionRay,
    Point3,
    Vec3,
    NodePath,
    BitMask32,
    )
from panda3d.physics import (
    PhysicsCollisionHandler,
    ActorNode)

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


#
# PHYSICS FUNCTIONS
#
class Physics:
    def __init__(self):
        self.rayCTrav = CollisionTraverser("collision traverser for ray tests")
        #self.pusher = PhysicsCollisionHandler()
        self.pusher = CollisionHandlerPusher()
        self.pusher.addInPattern('%fn-in-%in')
        self.pusher.addOutPattern('%fn-out-%in')
        self.pusher.addInPattern('%fn-in')
        self.pusher.addOutPattern('%fn-out')

    def startPhysics(self):
        #self.actorNode = ActorNode("playerPhysicsControler")
        #base.physicsMgr.attachPhysicalNode(self.actorNode)
        #self.actorNode.getPhysicsObject().setMass(self.player_mass)
        #self.mainNode = render.attachNewNode(self.actorNode)
        self.mainNode = render.attachNewNode("CharacterColliders")
        self.reparentTo(self.mainNode)

        charCollisions = self.mainNode.attachNewNode(CollisionNode(self.char_collision_name))
        #charCollisions.node().addSolid(CollisionSphere(0, 0, self.player_height/4.0, self.player_height/4.0))
        #charCollisions.node().addSolid(CollisionSphere(0, 0, self.player_height/4.0*3.05, self.player_height/4.0))
        charCollisions.node().addSolid(CollisionSphere(0, 0, self.player_height/2.0, self.player_height/4.0))
        charCollisions.node().setIntoCollideMask(BitMask32(0x80))  # 1000 0000
        if self.show_collisions:
            charCollisions.show()
        self.pusher.addCollider(charCollisions, self.mainNode)
        base.cTrav.addCollider(charCollisions, self.pusher)

        charFFootCollisions = self.attachNewNode(CollisionNode("floor_ray"))
        #charFFootCollisions.node().addSolid(CollisionSegment((0,0,0), (0, 0, -2)))
        charFFootCollisions.node().addSolid(CollisionRay(0, 0, 0, 0, 0, -1))
        #charFFootCollisions.node().setIntoCollideMask(BitMask32(0x80))  # 1000 0000
        charFFootCollisions.node().setFromCollideMask(BitMask32(0x7f))  # 0111 1111
        charFFootCollisions.show()

        self.floor_handler = CollisionHandlerFloor()
        self.floor_handler.addCollider(charFFootCollisions, self.mainNode)
        base.cTrav.addCollider(charFFootCollisions, self.floor_handler)

        self.accept("{}-in".format(self.char_collision_name), self.checkCharCollisions)

        self.raytest_segment = CollisionSegment(0, 1)
        self.raytest_np = render.attachNewNode(CollisionNode("testRay"))
        self.raytest_np.node().addSolid(self.raytest_segment)
        self.raytest_np.node().setFromCollideMask(BitMask32(0x7f))  # 0111 1111
        if self.show_collisions:
            self.raytest_np.show()

        self.raytest_queue = CollisionHandlerQueue()
        self.rayCTrav.addCollider(self.raytest_np, self.raytest_queue)

    def stopPhysics(self):
        self.raytest_segment.removeNode()
        self.pusher.clearColliders()
        self.floor_handler.clearColliders()
        self.rayCTrav.clearColliders()

    def updatePlayerPos(self, speed, heading, dt):
        if heading is not None:
            self.mainNode.setH(camera, heading)
            self.mainNode.setP(0)
            self.mainNode.setR(0)
        self.mainNode.setFluidPos(self.mainNode, speed)
        self.doStep()

    def checkCharCollisions(self, args):
        self.doStep()

    def doStep(self):
        # do the step height check
        tmpNP = self.mainNode.attachNewNode("temporary")
        tmpNP.setPos(self.mainNode, 0, 0, -self.stepheight)
        pointA = self.mainNode.getPos(render)
        pointA.setZ(pointA.getZ() + self.player_height/1.8)
        pointB = tmpNP.getPos(render)
        if pointA == pointB: return
        char_step_collision = self.getFirstCollisionInLine(pointA, pointB)
        tmpNP.removeNode()
        if char_step_collision is not None:
            self.mainNode.setFluidZ(char_step_collision.getZ())
            return True
        return False

    def getFirstCollisionInLine(self, pointA, pointB):
        """A simple raycast check which will return the first collision point as
        seen from point A towards pointB"""
        self.raytest_segment.setPointA(pointA)
        self.raytest_segment.setPointB(pointB)
        self.rayCTrav.traverse(render)
        self.raytest_queue.sortEntries()
        pos = None
        if self.raytest_queue.getNumEntries() > 0:
            pos = self.raytest_queue.getEntry(0).getSurfacePoint(render)
        return pos
