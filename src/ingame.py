#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import uuid
import collections

import pi3d

import replika.layer
import replika.assets
import replika.physics


class Scene(object):
    '''
    Game scene controller
    '''
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.__scene_active = True
        self.camera = game.camera
        self.shader = game.shader
        self.layers = collections.OrderedDict()
        self.layers['background'] = replika.layer.Layer('background', self)
        self.__current_layer = 'background'

    @property
    def default_layer(self):
        return self.layers[self.__current_layer]

    def new_layer(self, layer_name=None, layer_type=replika.layer.Layer):
        if layer_name is None:
            layer_name = str(uuid.uuid4())
        new_layer = layer_type(layer_name, self)
        self.layers[layer_name] = new_layer
        return new_layer

    def set_default_layer(self, layer):
        if isinstance(layer, replika.layer.Layer):
            layer = layer.name
        self.__current_layer = layer

    def remove_layer(self, layer_name):
        if layer_name == self.__current_layer:
            raise Exception('Cannot remove default layer')
        del(self.layers[layer_name])

    @property
    def is_running(self):
        return self.__scene_active and self.game.is_running

    def quit(self):
        self.__scene_active = False

    @property
    def fps(self):
        return self.game.fps

    def add_asset(self, element, position=None, name=None, layer=None):
        layer = self.default_layer if layer is None else self.layers[layer]
        return layer.add_asset(element, position, name)

    def update(self):
        for layer in reversed(self.layers.values()):
            layer.update()


class InGameElement(object):
    def __init__(self, layer, name):
        self.name = name
        self.layer = layer
        self.__living = True
        self._body_ = replika.physics.NoBody()

    @property
    def body(self):
        return self._body_

    @body.setter
    def body(self, new_body):
        position = self._body_.position
        self._body_ = new_body
        self._body_.position = position
        if isinstance(self.layer, replika.layer.PhysicsLayer):
            self.layer.world.add_element(self)

    @property
    def is_live(self):
        return self.__living

    def kill(self):
        if isinstance(self.layer, replika.layer.PhysicsLayer):
            self.layer.world.remove_element(self)
        self.__living = False

    def update(self):
        pass

    def collision(self, other_element):
        pass


class Image(InGameElement):
    def __init__(self, image_asset, layer, name,
                 position=None, distance=5.0):
        # Avoid errors in destructors (quick'n'dirty)
        if image_asset is None:
            # Create empty image
            image_asset = replika.assets.new_image((10, 10))
        super(Image, self).__init__(layer, name)
        if position is None:
            if image_asset.position is not None:
                self.body.position = image_asset.position
            else:
                self.body.position = (0, 0)
        else:
            self.body.position = position
        self.z = distance
        self.image = pi3d.ImageSprite(image_asset.texture,
                                      layer.shader,
                                      w=image_asset.width,
                                      h=image_asset.height,
                                      x=self.body.x, y=self.body.y,
                                      z=self.z, camera=layer.camera)
                
    def update(self):
        self.image.position(self.body.x + self.layer.offset[0],
                            self.body.y + self.layer.offset[1], self.z)
        self.image.draw()


class Animation(Image):
    def __init__(self, animation_asset, layer, name,
                 position=None, distance=5.0, fps=None):
        super(Animation, self).__init__(animation_asset.first_frame,
                                        layer, name, position, distance)
        self.images = [
            pi3d.ImageSprite(
                frame.texture, layer.shader,
                w=frame.width, h=frame.height,
                x=self.body.x, y=self.body.y, z=self.z,
                camera=layer.camera
            ) for frame in animation_asset.images
        ]
        self.frames = len(self.images)
        self.current_frame = 0
        self.current_tick = 0

        self.__fps = None
        if fps is None:
            if animation_asset.fps is None:
                self.fps = layer.scene.fps
            else:
                self.fps = animation_asset.fps
        else:
            self.fps = fps
        self.persistent = animation_asset.persistent

    @property
    def is_finished(self):
        return (self.current_frame >= self.frames - 1)
    
    def reset(self):
        self.current_frame = 0
        self.current_tick = 0

    @property
    def fps(self):
        return self.__fps

    @fps.setter
    def fps(self, fps):
        self.__fps = fps
        self.__ticks_per_frm = round(float(self.layer.scene.fps)/float(fps))

    def update(self):
        self.current_tick += 1
        if self.current_tick >= self.__ticks_per_frm:
            self.advance_frame()
        self.images[self.current_frame].position(
            self.body.x + self.layer.offset[0],
            self.body.y + self.layer.offset[1], self.z)
        self.images[self.current_frame].draw()

    def advance_frame(self):
        self.current_tick = 0
        if self.current_frame >= self.frames - 1:
            if not self.persistent:
                self.kill()
            return
        self.current_frame += 1


class Loop(Animation):
    def __init__(self, animation_asset, layer, name, position=None,
                 distance=5.0, fps=None):
        super(Loop, self).__init__(
            animation_asset, layer, name, position, distance, fps)
            
    @property
    def is_finished(self):
        return False
    
    def advance_frame(self):
        self.current_tick = 0
        self.current_frame += 1
        if self.current_frame >= self.frames:
            self.current_frame = 0


def action(action_method):
    def new_function(obj):
        action_name = action_method.__name__
        obj.set_state(action_name)
        action_method(obj)
    return new_function


class Puppet(InGameElement):
    def __init__(self, puppet_asset, layer, name, position=None,
                 distance=5.0):
        super(Puppet, self).__init__(layer, name)
        self._body_ = replika.physics.NoBody()
        self.animations = {}
        self.body.position = position
        self.distance = distance
        self.__current_state = 'initial'
        for action in puppet_asset.actions:
            self.animations[action] = self._ingame_(puppet_asset[action])
            self.animations[action].body = self.body

    @property
    def body(self):
        return self._body_

    @body.setter
    def body(self, new_body):
        position = self._body_.position
        self._body_ = new_body
        self._body_.position = position
        for animation in self.animations.values():
            animation.body = self.body
        if isinstance(self.layer, replika.layer.PhysicsLayer):
            self.layer.world.add_element(self)
        
    def _ingame_(self, animation_asset):
        if isinstance(animation_asset, replika.assets.Loop):
            return Loop(animation_asset, self.layer, self.name,
                        position=self.body.position,
                        distance=self.distance)
        elif isinstance(animation_asset, replika.assets.Animation):
            return Animation(animation_asset, self.layer, self.name,
                             position=self.body.position,
                             distance=self.distance)
        raise ValueError

    @property
    def is_live(self):
        if self.__current_state == 'final':
            return not self.current_animation.is_finished
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
        if animation == self.__current_state:
            return True
        self.__current_state = animation
        self.current_animation.reset()
        return True

    def reset(self):
        self._switch_animation_('initial')

    def kill(self):
        super(Puppet, self).kill()
        self._switch_animation_('final')

    @property
    def fps(self):
        return self.current_animation.fps

    @fps.setter
    def fps(self, fps):
        self.current_animation.fps = fps

    def update(self):
        self.current_animation.update()

#
# Factory
#
def new(asset, layer, name, position):
    if isinstance(asset, replika.assets.Image):
        return replika.ingame.Image(asset, layer, name, position)
    elif isinstance(asset, replika.assets.Loop):
        return replika.ingame.Loop(asset, layer, name, position)
    elif isinstance(asset, replika.assets.Animation):
        return replika.ingame.Animation(asset, layer, name, position)
    elif isinstance(asset, replika.assets.Puppet):
        return (replika.ingame.Puppet(asset, layer, name, position)
                if asset.behaviour is None else
                asset.behaviour(asset, layer, name, position))
    else:
        raise ValueError(asset)
