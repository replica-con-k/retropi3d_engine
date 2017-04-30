#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import uuid
import collections

import pi3d


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

    def put_animation(self, animation, position=(0, 0), loop=False,
                      fps=None, name=None):
        return self.__add_element__(
            Animation(animation, self, name, position, fps=fps, loop=loop))

    def spawn_puppet(self, puppet_animations, position=(0, 0),
                     fps=None, name=None):
        return self.__add_element__(
            Puppet(puppet_animations, self, name, position, fps=fps))

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
    def __init__(self, texture, scene, name,
                 position=(0, 0), distance=5.0):
        super(Image, self).__init__(scene, name)
        self.x, self.y = position
        self.z = distance
        self.image = pi3d.ImageSprite(texture,
                                      scene.shader,
                                      w=texture.ix, h=texture.iy,
                                      x=self.x, y=self.y, z=self.z,
                                      camera=scene.camera)
                
    def update(self):
        self.image.position(self.x, self.y, self.z)
        self.image.draw()


class Animation(Image):
    def __init__(self, textures, scene, name, position=(0, 0), distance=5.0,
                 fps=None, loop=None, autokill=False):
        super(Animation, self).__init__(textures[0], scene, name, position,
                                        distance)
        self.images = [
            pi3d.ImageSprite(
                frame, scene.shader,
                w=frame.ix, h=frame.iy,
                x=self.x, y=self.y, z=self.z,
                camera=scene.camera) for frame in list(filter(
                    (lambda x: x is not None), textures))
        ]
        if textures[-1] is None:
            self.images += [None]
        self.__frames = len(self.images)
        self.__current_frame = 0
        self.__current_tick = 0
        self.__fps = None
        self.fps = scene.fps if fps is None else fps
        if loop is not None:
            self.loop = loop
            
    @property
    def finished(self):
        return (self.__current_frame + 1 >= self.__frames) and not self.loop
    
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
        self.__ticks_per_frm = round(float(self.scene.fps)/float(fps))

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
                

class Puppet(InGameElement):
    def __init__(self, action_frames, scene, name,
                 position=(0, 0), distance=5.0, fps=None):
        super(Puppet, self).__init__(scene, name)
        assert(isinstance(action_frames, dict))
        assert('initial' in action_frames.keys())
        self.animations = {
            'initial': Animation(
                action_frames['initial'], scene, name, position, distance, fps)
        }
        for action in action_frames.keys():
            if action == 'initial':
                continue
            self.animations[action] = Animation(
                action_frames[action], scene, name, position, distance, fps)
        self.__current_state = 'initial'
        
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
        if self.current_state == 'final':
            return False
        if state == self.current_state:
            return True
        if state not in self.animations.keys():
            return False
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
