#!/usr/bin/env python
#

import math

import replika.assets


def create_body(asset_element, position=(0, 0)):
    return Body(asset_element.size, position)
        

class NoBody(object):
    def __init__(self, position=(0, 0)):
        self._x, self._y = position

    @property
    def position(self):
        return (self._x, self._y)

    @position.setter
    def position(self, new_position):
        self._x, self._y = new_position
        
    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, new_column):
        self._x = new_column

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, new_row):
        self._y = new_row

        
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
    def __init__(self, collision_cb):
        self.collision_cb = collision_cb
        self.bodies = {}

    def add_element(self, element):
        self.bodies[element.name] = element.body

    def remove_element(self, element):
        if element.name in self.bodies.keys():
            del(self.bodies[element.name])

    def _collide_(self, body1, body2):
        return (
            (math.fabs(body1.x - body2.x) * 2.0) < (body1.width + body2.width)
            and
            (math.fabs(body1.y - body2.y) * 2.0) < (body1.height + body2.height)
        )
        
    def update(self):
        processed = {}
        for body_name in self.bodies.keys():
            body = self.bodies[body_name]
            if not isinstance(body, Body):
                continue
            for already_processed in processed.keys():
                if self._collide_(body, already_processed):
                    self.collision_cb(body_name,
                                      processed[already_processed])
            processed[body] = body_name
