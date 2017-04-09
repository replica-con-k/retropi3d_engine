#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import uuid
import pi3d
import cymunk
import collections

# For now...
FPS = 20
DEFAULT_SHADER = "uv_flat"


def load(image_files):
    '''
    Load one or more images, return single or list Texture() objects
    '''
    def _load_single_(image_file):
        return pi3d.Texture(image_file)
    if isinstance(image_files, str) or isinstance(image_files, unicode):
        return _load_single_(image_files)
    else:
        # Yep, don't check if it's iterable or not :O
        return [_load_single_(image) for image in image_files]


class World(object):
    def __init__(self, size, shader_name=None):
        width, height = size
        self.display = pi3d.Display.create(w=width, h=height,
                                           frames_per_second=FPS)
        self.space = cymunk.Space()       
        self.camera = pi3d.Camera(is_3d=False)        
        self.shader = pi3d.Shader(shader_name or DEFAULT_SHADER)
        self.sprites = {}

    def new_image(self, image, position=(0, 0), name=None):
        name = name or str(uuid.uuid4())
        self.sprites[name] = Image(image, self, position)
        return name

    def loop_running(self):
        if self.display is None:
            return False
        return self.display.loop_running()

    def destroy(self):
        if self.display is None:
            return
        self.display.destroy()
        self.display = None

    def __del__(self):
        self.destroy()

    def update(self):
        self.space.step(1.0 / (FPS / 3.0))
        for sprite in self.sprites.values():
            sprite.update()


class Image(object):
    def __init__(self, frame, world, position=(0, 0), distance=5.0):
        self.x, self.y = position
        self.z = distance
        self.image = pi3d.ImageSprite(frame,
                                      world.shader,
                                      w=frame.ix, h=frame.iy,
                                      x=self.x, y=self.y, z=self.z,
                                      camera=world.camera)
        self.world = world
                
    def update(self):
        self.image.position(self.x, self.y, self.z)
        self.image.draw()


class Animation(Image):
    def __init__(self, frames, world, position=(0, 0), distance=5.0, fps=FPS):
        super(Image, self).__init__(frame[0], world, position, distance)
        self.images = [
            pi3d.ImageSprite(frame,
                             world.shader,
                             w=frame.ix, h=frame.iy,
                             x=self.x, y=self.y, z=self.z,
                             camera=world.camera) for frame in frames]
        self.__last_frame = len(self.images)
        self.__current_frame = 0
        self.__current_tick = 0
        self.__fps = fps
        self.__end_cb = None
        self.fps = fps

    def set_end_callback(self, cb):
        self.__end_cb = cb

    def reset(self):
        self.__current_frame = 0
        self.__current_tick = 0
        
    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, fps):
        self.__fps = fps
        self.__ticks_per_frm = round(
            float(FPS)/float(fps))

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
            self.__current_frame -= 1
            if self.__end_cb is not None:
                if self.__end_cb():
                    self.__current_frame = 0