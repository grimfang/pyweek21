#!/usr/bin/python
# -*- coding: utf-8 -*-

from direct.interval.LerpInterval import LerpFunc
from direct.interval.IntervalGlobal import Sequence, Parallel, Func, Wait

__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""


#
# CAMERA FUNCTIONS
#
class Animator:
    def __init__(self):
        self.current_animations = []
        self.enterRunDuration = 1.5
        self.enterWalkDuration = 0.5

        self.skipPlayRateChanges = [self.IDLE]

        self.ease_in_idle = LerpFunc(
            self.easeAnimation,
            fromData=0,
            toData=1,
            blendType="easeIn",
            extraArgs=[self.IDLE])
        self.ease_out_idle = LerpFunc(
            self.easeAnimation,
            fromData=1,
            toData=0,
            blendType="easeOut",
            extraArgs=[self.IDLE])

        self.ease_in_walk = LerpFunc(
            self.easeAnimation,
            fromData=0,
            toData=1,
            duration=self.enterWalkDuration,
            blendType="noBlend",
            extraArgs=[self.WALK])
        self.ease_out_walk = LerpFunc(
            self.easeAnimation,
            fromData=1,
            toData=0,
            blendType="noBlend",
            extraArgs=[self.WALK])

    def easeAnimation(self, t, anim):
        self.setControlEffect(anim, t)

    def setCurrentAnimsPlayRate(self, rate):
        """Set the play rate of the current playing animations to rate"""
        for anim in self.current_animations:
            if anim in self.skipPlayRateChanges:
                continue
            self.setPlayRate(rate, anim)
        self.walk_sound.setPlayRate(rate)

    def tryRequest(self, state):
        if not self.isInTransition():
            if not self.state == state:
                self.request(state)

    def enterIdle(self):
        self.current_animations = [self.IDLE]
        self.walk_sound.stop()
        if not self.getCurrentAnim() == self.IDLE:
            self.loop(self.IDLE)

    def enterWalk(self):
        self.current_animations = [self.WALK]
        self.walk_sound.play()
        if not self.getCurrentAnim() == self.WALK:
            self.loop(self.WALK)

    def enterIdleToWalk(self):
        self.current_animations = [self.IDLE, self.WALK]
        self.ease_out_idle.duration = self.enterWalkDuration
        self.walk_sound.play()
        self.current_seq = Sequence(
            Func(self.enableBlend),
            Func(self.loop, self.WALK),
            Parallel(
                self.ease_out_idle,
                self.ease_in_walk),
            Func(self.stop, self.IDLE),
            Func(self.disableBlend),
            Func(self.tryRequest, self.STATE_WALK))
        self.current_seq.start()
    def exitIdleToWalk(self):
        self.stop(self.IDLE)
        if self.current_seq is not None:
            self.current_seq.finish()

    def enterWalkToIdle(self):
        self.current_animations = [self.WALK, self.IDLE]
        self.ease_out_walk.duration = self.current_accleration/self.max_accleration
        self.ease_in_idle.duration = self.current_accleration/self.max_accleration
        self.walk_sound.play()
        self.current_seq = Sequence(
            Func(self.enableBlend),
            Func(self.loop, self.IDLE),
            Parallel(
                self.ease_out_walk,
                self.ease_in_idle),
            Func(self.stop, self.WALK),
            Func(self.disableBlend),
            Func(self.tryRequest, self.STATE_IDLE))
        self.current_seq.start()
    def exitWalkToIdle(self):
        self.stop(self.WALK)
        if self.current_seq is not None:
            self.current_seq.finish()

    def enterPlant(self):
        self.current_animations = [self.PLANT]
        if not self.getCurrentAnim() == self.PLANT:
            self.current_seq = Sequence(
                self.actorInterval(self.PLANT, False),
                Func(self.tryRequest, self.STATE_IDLE))
            self.current_seq.start()
    def exitPlant(self):
        if self.current_seq is not None:
            self.current_seq.finish()
