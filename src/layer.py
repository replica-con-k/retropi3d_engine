#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import uuid
import collections

import replika.assets
import replika.ingame
import replika.physics

class Layer(object):
    '''
    This class is just a InGame elements container
    '''
    def __init__(self, name=None, scene=None):
        self.name = name or str(uuid.uuid4())
        self.scene = scene
        self.elements = collections.OrderedDict()
        self.offset = (0, 0)

    @property
    def shader(self):
        return self.scene.shader

    @property
    def camera(self):
        return self.scene.camera

    def add_asset(self, asset, position=None, name=None):
        name = name or str(uuid.uuid4())
        if isinstance(asset, replika.assets.Image):
            element = replika.ingame.Image(asset, self, name, position)
        elif isinstance(asset, replika.assets.Loop):
            element = replika.ingame.Loop(asset, self, name, position)
        elif isinstance(asset, replika.assets.Animation):
            element = replika.ingame.Animation(asset, self, name, position)
        elif isinstance(asset, replika.assets.Puppet):
            element = (replika.ingame.Puppet(asset, self, name, position)
                       if asset.behaviour is None else
                       asset.behaviour(asset, self, name, position))
        else:
            raise ValueError(asset)
        self.elements[element.name] = element
        return element

    def remove(self, element):
        if isinstance(element, replika.ingame.InGameElement):
            element = element.name
        del(self.elements[element])

    def update(self):
        dead_elements = []
        for element in reversed(self.elements.values()):
            if element.is_live:
                element.update()
            else:
                dead_elements.append(element.name)
        for element in dead_elements:
            self.remove(element)
            

class PhysicsLayer(Layer):
    '''
    A Layer with world and collision handler
    '''
    def __init__(self, name=None, scene=None):
        super(PhysicsLayer, self).__init__(name, scene)
        self.world = replika.physics.World(self.notify_collision)

    def add_asset(self, asset, position=None, name=None):
        element = super(PhysicsLayer, self).add_asset(asset, position, name)
        self.world.add_element(element)
        return element

    def update(self):
        self.world.update()
        super(PhysicsLayer, self).update()

    def notify_collision(self, element1, element2):
        element1 = self.elements[element1]
        element2 = self.elements[element2]
        element1.collision(element2)
        element2.collision(element1)
        
