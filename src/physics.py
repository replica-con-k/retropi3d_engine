#!/usr/bin/env python
#

import replika.assets


def create_body(asset_element, position=(0, 0)):
    return Body([(0, 0), asset_element.size], position)
        

class Body(object):
    def __init__(self, skeleton, position=(0, 0), mass=None):
        '''
        skeleton is a seq of points (poly), this body is the
        bounding box of points.
        '''
        x0 = min([p[0] for p in skeleton])
        y0 = min([p[1] for p in skeleton])
        x1 = max([p[0] for p in skeleton])
        y1 = max([p[1] for p in skeleton])
        self.width = x1 - x0
        self.height = y1 - y0
        self.mass = mass
        self.position = position

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]
    

class World(object):
    def __init__(self):
        self.__bodies = {}
