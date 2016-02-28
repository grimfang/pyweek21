#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# PANDA3D ENGINE IMPORTS
#
from panda3d.core import PandaNode

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


#
# CAMERA FUNCTIONS
#
class Camera:
    def __init__(self, near=0.5, far=5000, fov=90):
        # set the minimum and maximum view distance
        base.camLens.setNearFar(near, far)
        base.camLens.setFov(fov)

    def startCamera(self):
        """Starts the camera module."""
        # to enhance readability
        self.cam_floater = self.mainNode
        self.cam_floater = self.mainNode.attachNewNode(PandaNode("playerCamFloater"))
        self.cam_floater.setPos(self.cam_floater_pos)
        taskMgr.add(self.updateCamera, "task_camActualisation", priority=-4)

    def stopCamera(self):
        taskMgr.remove("task_camActualisation")
        self.cam_floater.removeNode()

    def pauseCamera(self):
        taskMgr.remove("task_camActualisation")

    def resumeCamera(self):
        taskMgr.add(self.updateCamera, "task_camActualisation", priority=-4)

    def centerCamera(self):
        """This method will move the camera centered behind the player model"""
        # Camera Movement Updates
        camvec = self.cam_floater.getPos() - camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camdist = 3.0
        # get the cameras current offset to the player model on the z-axis
        offsetZ = self.cam_floater.getZ()
        camera.setPos(self.mainNode, 0, camdist, offsetZ)
        base.win.movePointer(0, self.win_width_half, self.win_height_half)
        camera.lookAt(self.cam_floater)

    def updateCamera(self, task):
        """This function will check the min and max distance of the camera to
        the defined model and will correct the position if the cam is to close
        or to far away"""


        # check if the camera should be centered
        if self.isDown(self.key_center_camera):
            self.centerCamera()
            return task.cont

        dt = globalClock.getDt()

        # Move camera left/right with the mouse
        if base.mouseWatcherNode.hasMouse() and self.enable_mouse:
            mw = base.mouseWatcherNode
            if base.win.movePointer(0, self.win_width_half, self.win_height_half):
                # Vertical positioning
                mouse_y = mw.getMouseY()
                z = mouse_y * self.mouse_speed_y * dt
                if self.mouse_invert_vertical:
                    camera.setZ(camera, z)
                else:
                    camera.setZ(camera, -z)

                # Horizontal positioning
                mouse_x = mw.getMouseX()
                x = mouse_x * self.mouse_speed_x * dt
                camera.setX(camera, -x)

        # Camera Movement Updates
        camvec = self.cam_floater.getPos(render) - camera.getPos(render)
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()

        # camera collision detection
        # always set the cameras position to the first hitpoint on a collision solid
        pos = self.getFirstCollisionInLine(self.cam_floater.getPos(render), camera.getPos(render))
        had_ray_collision = False
        if pos is not None:
            had_ray_collision = True
            camera.setPos(pos)

        # If the camera is to far from player start following
        if camdist > self.max_cam_distance:
            camera.setPos(camera.getPos()+camvec*(camdist-self.max_cam_distance))
            camdist = self.max_cam_distance

        # If player is to close move the camera backwards
        if camdist < self.min_cam_distance:
            if not had_ray_collision:
                # move the camera backwards
                camera.setPos(camera.getPos()-camvec*(self.min_cam_distance-camdist))
                camdist = self.min_cam_distance
            else:
                # we can't move the camera back into the wall, so move it up
                #TODO: Maybe change max_cam_height_distance with something like
                #      self.min_cam_dist - camdist
                camera.setZ(self.cam_floater.getZ() + self.max_cam_height_distance)

        # Get the cameras current offset to the player model on the z-axis
        offsetZ = camera.getZ(render) - self.cam_floater.getZ(render)
        # check if the camera is within the min and max z-axis offset
        if offsetZ < self.min_cam_height_distance:
            # the cam is to low, so move it up
            camera.setZ(self.cam_floater.getZ(render) + self.min_cam_height_distance)
            offsetZ = self.min_cam_height_distance
        elif offsetZ > self.max_cam_height_distance:
            # the cam is to high, so move it down
            camera.setZ(self.cam_floater.getZ(render) + self.max_cam_height_distance)
            offsetZ = self.max_cam_height_distance

        # lazy camera positioning
        # if we are not moving up or down, set the cam to an average position
        if offsetZ > self.cam_height_avg:
            # the cam is higher then the average cam height above the player
            # so move it slowly down
            camera.setZ(camera.getZ(render) - self.cam_z_justification_speed * globalClock.getDt())
            newOffsetZ = camera.getZ(render) - self.cam_floater.getZ()
            # check if the cam has reached the desired offset
            if newOffsetZ < self.cam_height_avg:
                # set the cam z position to exactly the desired offset
                camera.setZ(self.cam_floater.getZ(render) + self.cam_height_avg)
        elif offsetZ < self.cam_height_avg:
            # the cam is lower then the average cam height above the player
            # so move it slowly up
            camera.setZ(camera.getZ() + self.cam_z_justification_speed * globalClock.getDt())
            newOffsetZ = camera.getZ() - self.cam_floater.getZ(render)
            # check if the cam has reached the desired offset
            if newOffsetZ > self.cam_height_avg:
                # set the cam z position to exactly the desired offset
                camera.setZ(self.cam_floater.getZ(render) + self.cam_height_avg)

        camera.lookAt(self.cam_floater)
        return task.cont
