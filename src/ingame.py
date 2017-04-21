#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import uuid
import pi3d
import cymunk
import collections


class Image(object):
    def __init__(self, texture, game, name,
                 position=(0, 0), distance=5.0):
        self.x, self.y = position
        self.z = distance
        self.image = pi3d.ImageSprite(texture,
                                      game.shader,
                                      w=texture.ix, h=texture.iy,
                                      x=self.x, y=self.y, z=self.z,
                                      camera=game.camera)
        self.name = name
        self.game = game
                
    def update(self):
        self.image.position(self.x, self.y, self.z)
        self.image.draw()


class Animation(Image):
    def __init__(self, textures, game, name, position=(0, 0), distance=5.0,
                 fps=None, loop=False):
        super(Animation, self).__init__(textures[0], game, name, position,
                                        distance)
        self.images = [
            pi3d.ImageSprite(frame,
                             game.shader,
                             w=frame.ix, h=frame.iy,
                             x=self.x, y=self.y, z=self.z,
                             camera=game.camera) for frame in textures]
        self.__last_frame = len(self.images)
        self.__current_frame = 0
        self.__current_tick = 0
        self.__fps = None
        self.__loop = loop
        self.fps = game.fps if fps is None else fps

    @property
    def loop(self):
        return self.__loop

    @loop.setter
    def loop(self, loop):
        self.reset()
        self.__loop = loop
    
    def reset(self):
        self.__current_frame = 0
        self.__current_tick = 0
        
    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, fps):
        self.__fps = fps
        self.__ticks_per_frm = round(float(self.game.fps)/float(fps))

    def update(self):
        self.__current_tick += 1
        if self.__current_tick >= self.__ticks_per_frm:
            self.__advance_frame()
        self.images[self.__current_frame].position(self.x, self.y, self.z)
        self.images[self.__current_frame].draw()

    def __advance_frame(self):
        self.__current_tick = 0
        self.__current_frame += 1
        if self.__current_frame == self.__last_frame:
            self.__current_frame = 0 if self.__loop else (self.__last_frame - 1)
