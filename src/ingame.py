#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import uuid
import collections

import pi3d

import replika.assets

class Scene(object):
    def __init__(self, game, name):
        self.__game = game
        self.name = name
        self.__scene_active = True
        self.camera = game.camera
        self.shader = game.shader
        self.elements = collections.OrderedDict()

    @property
    def is_running(self):
        return self.__scene_active and self.__game.is_running

    def quit(self):
        self.__scene_active = False

    @property
    def fps(self):
        return self.__game.fps

    def __add_element__(self, element, name=None):
        name = name or str(uuid.uuid4())
        element.name = name
        self.elements[name] = element
        return element

    def __remove_element__(self, element):
        element_name = element.name if (
            isinstance(element, InGameElement)) else element
        del(self.elements[element_name])
       
    def put_image(self, image, position=(0, 0), name=None):
        return self.__add_element__(Image(image, self, name, position))

    def put_animation(self, animation, position=(0, 0), name=None,
                      persistent=True):
        if isinstance(animation, replika.assets.Loop):
            return self.__add_element__(
                Loop(animation, self, name, position))
        else:
            return self.__add_element__(
                Animation(animation, self, name, position,
                          persistent=persistent))

    def spawn_puppet(self, animations, position=(0, 0), name=None):
        return self.__add_element__(
            Puppet(animations, self, name, position))

    def update(self):
        dead_elements = []
        for element in reversed(self.elements.values()):
            if element.is_live:
                element.update()
            else:
                dead_elements.append(element.name)
        for element in dead_elements:
            self.__remove_element__(element)



class InGameElement(object):
    def __init__(self, scene, name):
        self.name = name
        self.scene = scene
        self.__living = True

    @property
    def is_live(self):
        return self.__living

    def kill(self):
        self.__living = False

    def update(self):
        pass


class Image(InGameElement):
    def __init__(self, image_asset, scene, name,
                 position=None, distance=5.0):
        super(Image, self).__init__(scene, name)
        if position is None:
            if image_asset.position is not None:
                self.x, self.y = image_asset.position
            else:
                self.x, self.y = (0, 0)
        else:
            self.x, self.y = position
        self.z = distance
        self.image = pi3d.ImageSprite(image_asset.texture,
                                      scene.shader,
                                      w=image_asset.width,
                                      h=image_asset.height,
                                      x=self.x, y=self.y, z=self.z,
                                      camera=scene.camera)
                
    def update(self):
        self.image.position(self.x, self.y, self.z)
        self.image.draw()


class Animation(Image):
    def __init__(self, animation_asset, scene, name,
                 position=None, distance=5.0, fps=None, persistent=True):
        super(Animation, self).__init__(animation_asset.first_frame,
                                        scene, name, position, distance)
        self.images = [
            pi3d.ImageSprite(
                frame.texture, scene.shader,
                w=frame.width, h=frame.height,
                x=self.x, y=self.y, z=self.z,
                camera=scene.camera
            ) for frame in animation_asset.images
        ]
        self.frames = len(self.images)
        self.current_frame = 0
        self.current_tick = 0

        if position is None:
            if animation_asset.position is None:
                self.x, self.y = (0, 0)
            else:
                self.x, self.y = animation_asset.position
        else:
            self.x, self.y = position

        self.__fps = None
        if fps is None:
            if animation_asset.fps is None:
                self.fps = scene.fps
            else:
                self.fps = animation_asset.fps
        else:
            self.fps = fps
        self.persistent = persistent

    @property
    def finished(self):
        return (self.current_frame + 1 >= self.frames)
    
    def reset(self):
        self.current_frame = 0
        self.current_tick = 0
        
    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, fps):
        self.__fps = fps
        self.__ticks_per_frm = round(float(self.scene.fps)/float(fps))

    def update(self):
        self.current_tick += 1
        if self.current_tick >= self.__ticks_per_frm:
            self.advance_frame()
        self.images[self.current_frame].position(self.x, self.y, self.z)
        self.images[self.current_frame].draw()

    def advance_frame(self):
        self.current_tick = 0
        if self.current_frame >= self.frames - 1:
            if not self.persistent:
                self.kill()
            return
        self.current_frame += 1


class Loop(Animation):
    def __init__(self, animation_asset, scene, name, position=None,
                 distance=5.0, fps=None):
        super(Loop, self).__init__(
            animation_asset, scene, name, position, distance, fps)
            
    @property
    def finished(self):
        return False
    
    def advance_frame(self):
        self.current_tick = 0
        self.current_frame += 1
        if self.current_frame >= self.frames:
            self.current_frame = 0


class Puppet(InGameElement):
    def __init__(self, puppet_asset, scene, name, position=None,
                 distance=5.0):
        super(Puppet, self).__init__(scene, name)
        self.animations = {}
        self.position = position
        self.distance = distance
        self.__current_state = 'initial'
        for action in puppet_asset.actions:
            self.animations[action] = self._ingame_(puppet_asset[action])

        
    def _ingame_(self, animation_asset):
        if isinstance(animation_asset, replika.assets.Loop):
            return Loop(animation_asset, self.scene, self.name,
                        position=self.position,
                        distance=self.distance)
        elif isinstance(animation_asset, replika.assets.Animation):
            return Animation(animation_asset, self.scene, self.name,
                             position=self.position,
                             distance=self.distance)
        raise ValueError

    @property
    def is_live(self):
        if self.__current_state == 'final':
            return not self.current_animation.finished
        return super(Puppet, self).is_live

    @property
    def current_animation(self):
        return self.animations[self.__current_state]

    @property
    def current_state(self):
        return self.__current_state

    def set_state(self, state):
        if ((self.current_state == 'final') or
            (state not in self.animations.keys())):
            return False
        if state == self.current_state:
            return True
        return self._switch_animation_(state)

    def _switch_animation_(self, animation):
        if animation not in self.animations.keys():
            return False
        self.__current_state = animation
        self.current_animation.reset()
        return True

    def reset(self):
        self._switch_animation_('initial')

    def kill(self):
        self._switch_animation_('final')
        super(Puppet, self).kill()

    @property
    def fps(self):
        return self.current_animation.fps

    @fps.setter
    def fps(self, fps):
        self.current_animation.fps = fps

    def update(self):
        self.current_animation.update()
