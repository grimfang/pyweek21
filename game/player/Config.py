#!/usr/bin/python
# -*- coding: utf-8 -*-

from panda3d.core import KeyboardButton, Point3F

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


#
# PLAYER CONFIGURATIONS
#
class Config:
    def __init__(self):
        #
        # MODEL AND ANIMATION
        #
        # The players model file path
        self.basePath = "character/"
        self.model = self.basePath + "character"
        # Paths of the animation files
        self.anim_idle = self.basePath + "character-Idle"
        self.anim_walk = self.basePath + "character-Walk"
        self.anim_plant = self.basePath + "character-Plant"
        # NOTE: This should always be enabled to smoth the transition within
        #       animations. For example for the accleration of the character
        #       untill it reaches full pace.
        self.enable_interpolation = True

        #
        # AUDIO
        #
        self.sfxPath = "sfx/"
        self.walk_sound = loader.loadSfx(self.sfxPath + "step.ogg")
        self.walk_sound.setLoop(True)


        #
        # CONTROLS
        #
        self.key_forward = KeyboardButton.asciiKey('w')
        self.key_backward = KeyboardButton.asciiKey('s')
        self.key_left = KeyboardButton.asciiKey('a')
        self.key_right = KeyboardButton.asciiKey('d')
        self.key_plant = KeyboardButton.space()
        self.key_center_camera = KeyboardButton.home()
        # accleration for the various states
        self.accleration = 3.5
        # the speed of how fast the player deacclerates
        self.deaccleration = 10.0
        # maximum acclerations at the various states
        self.max_accleration = 8.0
        # the speed for how fast the player is generally moving
        self.speed = 0.7

        #
        # GAME SPECIFIC
        #
        # planting possibility
        self.planting_enabled = False
        self.carry_seed = False

        #
        # CAMERA CONTROL VARIABLES
        #
        # Camera basics
        self.cam_near_clip = 0.5
        self.cam_far_clip = 5000
        self.cam_fov = 70
        # Mouse camera movement
        # enables the camera control via the mouse
        self.enable_mouse = True
        # invert vertical camera movements
        self.mouse_invert_vertical = False
        # screen sizes
        self.win_width_half = base.win.getXSize() / 2
        self.win_height_half = base.win.getYSize() / 2
        # mouse speed
        self.mouse_speed_x = 150.0
        self.mouse_speed_y = 80.0
        # the next two vars will set the min and max distance the cam can have
        # to the node it is attached to
        self.max_cam_distance = 5.0
        self.min_cam_distance = 2.0
        # the initial cam distance
        self.cam_distance = (self.max_cam_distance - self.min_cam_distance) / 2.0 + self.min_cam_distance
        # the maximum distance on the Z-Axis to the player
        self.max_cam_height_distance = 2.0
        # the minimum distance on the Z-Axis to the player
        self.min_cam_height_distance = 0.15
        # the average camera height
        self.cam_height_avg = (self.max_cam_height_distance - self.min_cam_height_distance) / 2.0 + self.min_cam_height_distance
        # the initial cam height
        self.cam_height = self.cam_height_avg
        # the speed of the cameras justification movement towards
        # the average height
        self.cam_z_justification_speed = 1
        # a floater which hovers over the player and is used as a
        # look at position for the camera
        self.cam_floater_pos = Point3F(0, 0, 1.5)

        #
        # PHYSICS
        #
        # show collision solids
        self.show_collisions = False
        # The physical physic_world which will be responsible for collision checks and
        # physic updates
        self.physic_world = None
        # the name of the collision solids that surround the character
        self.char_collision_name = "CharacterCollisions"
        # the mass of the character
        self.player_mass = 25
        # the heights of the various player states
        # normal height
        self.player_height = 1.186
        # the radius of the players collision shape
        self.player_radius = self.player_height / 4.0
        # step height
        self.stepheight = 0.7
