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
