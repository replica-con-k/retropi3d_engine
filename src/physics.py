#!/usr/bin/env python
#
import copy

import replika.assets


def create_body(asset_element, position=(0, 0)):
    return Body(asset_element.size, position)
        

class NoBody(object):
    def __init__(self, position=(0, 0)):
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = copy.copy(new_position)
        
    @property
    def x(self):
        return self._position[0]

    @x.setter
    def x(self, new_column):
        self._position = (new_column, self.position[1])

    @property
    def y(self):
        return self._position[1]

    @y.setter
    def y(self, new_row):
        self._position = (self.position[0], new_row)

        
class Body(NoBody):
    def __init__(self, size, position=(0, 0)):
        '''
        skeleton is a seq of points (poly), this body is the
        bounding box of points.
        '''
        super(Body, self).__init__(position)
        self.width = size[0]
        self.height = size[1]

    @property
    def size(self):
        return (self.width, self.height)

    def __hash__(self):
        return hash((self.position, self.size))
    

class World(object):
    def __init__(self, scene):
        self.scene = scene
        self.bodies = {}

    def add_element(self, element):
        self.bodies[element.name] = element.body

    def _collide_(self, body1, body2):
        return ((body1.x < body2.x + body2.width) and
                (body1.x + body1.width > body2.x) and
                (body1.y < body2.y + body2.height) and
                (body1.height + body1.y > body2.y))
        
    def update(self):
        processed = {}
        for body_name in self.bodies.keys():
            body = self.bodies[body_name]
            for already_processed in processed.keys():
                if self._collide_(body, already_processed):
                    self.scene.notify_collision(body_name,
                                                processed[already_processed])
            processed[body] = body_name
