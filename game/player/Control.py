#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PYTHON IMPORTS
#
import math

#
# PANDA3D ENGINE IMPORTS
#
from panda3d.core import Vec3, Point3F

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


#
# MOVE FUNCTIONS
#
class Control:
    def __init__(self):
        # the actual accleration the character is at
        self.current_accleration = 0.0
        self.movementVec = Vec3(0, 0, 0)

    def startControl(self):
        """Start the control module"""
        taskMgr.add(self.move, "task_movement", priority=-15)

    def stopControl(self):
        taskMgr.remove("task_movement")

    def move(self, task):
        """The main task for updating the players position according
        to the keys pressed by the user"""

        if self.state == self.STATE_PLANT:
            return task.cont

        dt = globalClock.getDt()
        isMoving = False
        requestState = None
        accleration_mult = 1.0
        isMoving = self.current_accleration > 0
        rotation = None

        #
        # PLAYER MOVEMENT
        #
        if self.isDown(self.key_forward):
            if self.movementVec.getY() == 1:
                self.current_accleration /= 4.0
            self.movementVec.setY(-1)
        elif self.isDown(self.key_backward):
            if self.movementVec.getY() == -1:
                self.current_accleration /= 4.0
            self.movementVec.setY(1)
        else:
            self.movementVec.setY(0)

        if self.isDown(self.key_left):
            if self.movementVec.getX() == 1:
                self.current_accleration /= 4.0
            self.movementVec.setX(-1)
        elif self.isDown(self.key_right):
            if self.movementVec.getX() == -1:
                self.current_accleration /= 4.0
            self.movementVec.setX(1)
        else:
            self.movementVec.setX(0)

        moveKeyPressed = self.movementVec != Vec3()
        if moveKeyPressed:
            isMoving = True
            # calculate the players heading
            angle = math.atan2(self.movementVec.getX(), self.movementVec.getY())
            rotation = angle * (180.0 / math.pi)
            # acclerate until we reached the maximum speed
            if self.current_accleration < self.max_accleration:
                self.current_accleration += self.accleration * dt
                if self.current_accleration > self.max_accleration:
                    self.current_accleration = self.max_accleration
            elif self.current_accleration > self.max_accleration:
                self.current_accleration -= self.deaccleration * dt
                if self.current_accleration < self.max_accleration:
                    self.current_accleration = self.max_accleration
            # set animation
            if self.state == self.STATE_IDLE and moveKeyPressed:
                requestState = self.STATE_IDLE_TO_WALK
            elif self.state == self.STATE_WALK_TO_IDLE and moveKeyPressed:
                requestState = self.STATE_WALK
        elif self.current_accleration > 0:
            if self.state == self.STATE_WALK:
                requestState = self.STATE_WALK_TO_IDLE
            # deacclerate until we stopped completely again
            self.current_accleration -= self.deaccleration * dt
            if self.current_accleration < 0:
                self.current_accleration = 0

        if self.current_accleration <= 0:
            if self.state == self.STATE_WALK:
                requestState = self.STATE_WALK_TO_IDLE
        else:
            self.setCurrentAnimsPlayRate(self.current_accleration/self.max_accleration)

        if self.isDown(self.key_plant) and self.planting_enabled:
            if self.STATE_PLANT in self.defaultTransitions[self.state]:
                self.doPlant()
                self.current_accleration = 0.0
                requestState = self.STATE_PLANT

        tmpNP = self.mainNode.attachNewNode("temporary")
        tmpNP.setPos(self.mainNode, 0, -2, 0)
        pointA = self.mainNode.getPos()
        pointA.setZ(self.mainNode.getZ() + self.player_height)
        pointB = tmpNP.getPos(render)
        pointB.setZ(self.mainNode.getZ() + self.player_height)
        char_front_collision = self.getFirstCollisionInLine(pointA, pointB)
        tmpNP.removeNode()
        if char_front_collision is not None:
            colvec = char_front_collision - self.mainNode.getPos()
            colvec.setZ(0)
            coldist = colvec.length()
            if coldist <= self.player_radius / 3.5:
                # we have a wall in front of us, hence we can't move forward
                self.current_accleration = 0
            elif moveKeyPressed:
                self.current_accleration -= self.deaccleration * dt
                if self.current_accleration < 0:
                    self.current_accleration = 0.0
            if self.state == self.STATE_WALK:
                requestState = self.STATE_WALK_TO_IDLE
            else:
                requestState = None

        if requestState:
            self.request(requestState)

        #
        # PLAYER UPDATE
        #
        # calculate the players forward movement speed
        self.current_speed = self.speed * self.current_accleration * dt
        self.updatePlayerPos((0, -self.current_speed, 0), rotation, dt)

        return task.cont
