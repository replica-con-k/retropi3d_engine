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
                 fps=None, loop=None):
        super(Animation, self).__init__(textures[0], game, name, position,
                                        distance)
        self.images = [
            pi3d.ImageSprite(frame,
                             game.shader,
                             w=frame.ix, h=frame.iy,
                             x=self.x, y=self.y, z=self.z,
                             camera=game.camera) for frame in textures]
        self.__frames = len(self.images)
        self.__current_frame = 0
        self.__current_tick = 0
        self.__fps = None
        self.fps = game.fps if fps is None else fps
        if loop is not None:
            self.loop = loop
            
    @property
    def loop(self):
        return self.images[-1] is None

    @loop.setter
    def loop(self, loop):
        self.reset()
        if loop:
            if self.images[-1] is not None:
                self.images += [None]
                self.__frames += 1
        else:
            if self.images[-1] is None:
                self.images = self.images[:-1]
                self.__frames -= 1
    
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
        if self.__current_frame >= self.__frames:
            self.__current_frame = self.__frames - 1
        if self.images[self.__current_frame] is None:
            self.__current_frame = 0
                

class Puppet(Animation):
    def __init__(self, action_frames, game, name,
                 position=(0, 0), distance=5.0, fps=None):
        assert(isinstance(action_frames, dict))
        assert('initial' in action_frames.keys())
        self.animations = {
            'initial': super(Puppet, self).__init__(
                action_frames['initial'], game, name, position, distance, fps)
        }
        for action in action_frames.keys():
            if action == 'initial':
                continue
            self.animations[action] = Animation(
                action_frames[action], game, name, position, distance, fps)
        self.__current_state = 'initial'
        self.game = game
        self.name = name
        
    @property
    def current_animation(self):
        return self.animations[self.__current_state]

    @property
    def current_state(self):
        return self.__current_state

    def set_state(self, state):
        if state not in self.animations.keys():
            return False
        self._switch_animation_(state)

    def _switch_animation_(self, animation):
        self.current_animation.reset()
        self.__current_state = animation

    def reset(self):
        self._switch_animation_('initial')

    @property
    def loop(self):
        return self.current_animation.loop

    @loop.setter
    def loop(self, loop):
        self.current_animation.loop = loop

    @property
    def fps(self):
        return self.current_animation.fps

    @fps.setter
    def fps(self, fps):
        self.current_animation.fps = fps

    def update(self):
        self.current_animation.update()
