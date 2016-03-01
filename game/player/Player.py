#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PYTHON IMPORTS
#
import logging

#
# PANDA3D ENGINE IMPORTS
#
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties

#
# CHARACTER SPECIFIC IMPORTS
#
from Config import Config
from Camera import Camera
from Control import Control
from PhysicsInternal import Physics
from Animator import Animator

__author__ = "MJ-meo-dmt & Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Player(FSM, Config, Physics, Actor, Camera, Control, Animator):

    # Names of the animations of the actor class
    IDLE = "Idle"
    WALK = "Walk"
    PLANT = "Plant"

    # PLAYER CLASS FSM STATES
    STATE_IDLE = "Idle"
    STATE_IDLE_TO_WALK = "IdleToWalk"
    STATE_WALK = "Walk"
    STATE_WALK_TO_IDLE = "WalkToIdle"
    STATE_PLANT = "Plant"

    def __init__(self, physic_world, config=None):
        logging.info("INIT PLAYER...")
        logging.info("INIT FSM...")
        FSM.__init__(self, "FSM-Player")
        logging.info("INIT CONFIG...")
        Config.__init__(self)
        # additional initial configuration settings set by the outher application
        self.physic_world = physic_world
        logging.info("INIT PHYSICS...")
        Physics.__init__(self)
        logging.info("INIT CONTROLS...")
        Control.__init__(self)
        logging.info("INIT CAMERA...")
        Camera.__init__(
            self,
            self.cam_near_clip,
            self.cam_far_clip,
            self.cam_fov)
        logging.info("INIT ANIMATOR...")
        Animator.__init__(self)
        logging.info("INIT PLAYER DONE")

        #
        # STATES SETUP
        #
        self.on_ground_states = [
            self.STATE_IDLE,
            self.STATE_IDLE_TO_WALK,
            self.STATE_WALK,
            self.STATE_WALK_TO_IDLE,
            self.STATE_PLANT]
        # set the possible transition in the FSM
        self.defaultTransitions = {
            self.STATE_IDLE: [self.STATE_IDLE_TO_WALK, self.STATE_PLANT],
            self.STATE_IDLE_TO_WALK: [self.STATE_IDLE, self.STATE_WALK],
            self.STATE_WALK: [self.STATE_IDLE, self.STATE_WALK_TO_IDLE],
            self.STATE_WALK_TO_IDLE: [self.STATE_IDLE, self.STATE_WALK],
            self.STATE_PLANT: [self.STATE_IDLE],
            }

        #
        # ACTOR SETUP
        #
        Actor.__init__(
            self,
            self.model,
            {
                self.IDLE: self.anim_idle,
                self.WALK: self.anim_walk,
                self.PLANT: self.anim_plant,
            })
        self.setBlend(frameBlend=self.enable_interpolation)

        #
        # CONTROLS SETUP
        #
        self.isDown = base.mouseWatcherNode.isButtonDown
        self.mainNode = self

    def catchCursor(self):
        # center the mouse in the middle of the window
        base.win.movePointer(0, self.win_width_half, self.win_height_half)
        # Set mouse mode to relative which should work best for our purpose
        wp = WindowProperties()
        wp.setMouseMode(WindowProperties.M_relative)
        base.win.requestProperties(wp)

    def freeCursor(self):
        # free the cursor
        wp = WindowProperties()
        wp.setMouseMode(WindowProperties.M_absolute)
        base.win.requestProperties(wp)

    def startPlayer(self):
        logging.debug("start player...")
        self.show()
        self.request(self.STATE_IDLE)
        logging.debug("...start physics...")
        self.startPhysics()
        logging.debug("...start coltrol...")
        self.startControl()
        logging.debug("...start camera...")
        self.startCamera()
        self.centerCamera()
        logging.debug("...player started")
        self.catchCursor()

    def stopPlayer(self):
        logging.debug("stop player...")
        logging.debug("...stop control...")
        self.stopControl()
        logging.debug("...stop camera...")
        self.stopCamera()
        logging.debug("...stop base...")
        self.freeCursor()
        # remove the actor
        Actor.cleanup(self)
        self.removeNode()
        logging.debug("...player stop")

    def pausePlayer(self):
        self.stopControl()
        self.pauseCamera()
        self.freeCursor()

    def resumePlayer(self):
        self.catchCursor()
        self.startControl()
        self.resumeCamera()

    def setStartPos(self, startPos):
        self.mainNode.setPos(startPos)

    def setStartHpr(self, startHpr):
        self.mainNode.setHpr(startHpr)

    def enablePlanting(self, enabled):
        self.planting_enabled = enabled

    def doPlant(self):
        base.messenger.send("player-plant_seed")

    def doPickupSeed(self, args):
        
        #
        pass

