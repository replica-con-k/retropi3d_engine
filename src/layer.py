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
        element = replika.ingame.new(asset, self, name, position)
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
        element1 = self.elements.get(element1, None)
        element2 = self.elements.get(element2, None)
        if element1 is not None:
            element1.collision(element2)
        if element2 is not None:
            element2.collision(element1)
        

class HorizontalScroll(Layer):
    '''
    A simple image background with infinite len
    '''
    def __init__(self, name=None, scene=None):
        self.background = None
        self._size = (0, 0)
        self._image_size = (0, 0)
        self._x_ofs = 0
        self._y_ofs = 0
        super(HorizontalScroll, self).__init__(name, scene)
        self.scene = scene

    @property
    def scene(self):
        return self.__scene

    @scene.setter
    def scene(self, scene):
        self.__scene = scene
        if scene is not None:
            self._size = (scene.game.display.width, scene.game.display.height)
            self._x_ofs = -self._size[0] / 2
            if self.background is not None:
                self._x_ofs -= (self._image_size[0] / 2)
            
    def add_asset(self, asset, position=(0, 0), name='background'):
        if name == 'background':
            self.background = replika.ingame.new(asset, self, name, position)
            self._image_size = asset.size
            return self.background
        return super(HorizontalScroll, self).add_asset(asset, position, name)

    def move(self, offset):
        self._x_ofs += offset[0]
        self._y_ofs += offset[1]

    def update(self):
        x_ofs = (self._x_ofs % self._image_size[0]) - self._size[0]
        y_ofs = self._y_ofs % self._image_size[1]
        while (x_ofs <= self._size[0]):
            self.background.image.position(x_ofs , y_ofs, 5.0)
            self.background.image.draw()
            x_ofs += self._image_size[0]
        super(HorizontalScroll, self).update()


class VerticalScroll(Layer):
    '''
    A simple image background with infinite len
    '''
    def __init__(self, name=None, scene=None):
        self.background = None
        self._size = (0, 0)
        self._image_size = (0, 0)
        self._x_ofs = 0
        self._y_ofs = 0
        super(VerticalScroll, self).__init__(name, scene)
        self.scene = scene

    @property
    def scene(self):
        return self.__scene

    @scene.setter
    def scene(self, scene):
        self.__scene = scene
        if scene is not None:
            self._size = (scene.game.display.width, scene.game.display.height)
            self._y_ofs = -self._size[1] / 2
            if self.background is not None:
                self._y_ofs -= (self._image_size[1] / 2)
            
    def add_asset(self, asset, position=(0, 0), name='background'):
        if name == 'background':
            self.background = replika.ingame.new(asset, self, name, position)
            self._image_size = asset.size
            return self.background
        return super(VerticalScroll, self).add_asset(asset, position, name)

    def move(self, offset):
        self._x_ofs += offset[0]
        self._y_ofs += offset[1]

    def update(self):
        x_ofs = (self._x_ofs % self._image_size[0])
        y_ofs = (self._y_ofs % self._image_size[1]) - self._size[1]
        while (y_ofs <= self._size[1]):
            self.background.image.position(x_ofs , y_ofs, 5.0)
            self.background.image.draw()
            y_ofs += self._image_size[1]
        super(VerticalScroll, self).update()


class Scroll(Layer):
    '''
    A simple image background with infinite len
    '''
    def __init__(self, name=None, scene=None):
        self.background = None
        self._size = (0, 0)
        self._image_size = (0, 0)
        self._x_ofs = 0
        self._y_ofs = 0
        super(Scroll, self).__init__(name, scene)
        self.scene = scene

    @property
    def scene(self):
        return self.__scene

    @scene.setter
    def scene(self, scene):
        self.__scene = scene
        if scene is not None:
            self._size = (scene.game.display.width, scene.game.display.height)
            self._x_ofs = -self._size[0] / 2
            self._y_ofs = -self._size[1] / 2
            if self.background is not None:
                self._x_ofs -= (self._image_size[0] / 2)
                self._y_ofs -= (self._image_size[1] / 2)
            
    def add_asset(self, asset, position=(0, 0), name='background'):
        if name == 'background':
            self.background = replika.ingame.new(asset, self, name, position)
            self._image_size = asset.size
            return self.background
        return super(Scroll, self).add_asset(asset, position, name)

    def move(self, offset):
        self._x_ofs += offset[0]
        self._y_ofs += offset[1]

    def update(self):
        x_ofs = (self._x_ofs % self._image_size[0]) - self._size[0]
        while (x_ofs <= self._size[0]):
            y_ofs = (self._y_ofs % self._image_size[1]) - self._size[1]
            while (y_ofs <= self._size[1]):
                self.background.image.position(x_ofs , y_ofs, 5.0)
                self.background.image.draw()
                y_ofs += self._image_size[1]
            x_ofs += self._image_size[0]
        super(Scroll, self).update()


class TileMap(Layer):
    '''
    A tile map image
    '''
    def __init__(self, tileset, size, name=None, scene=None):
        super(TileMap, self).__init__(name, scene)
        self.scene = scene
        self.tiles = tileset
        self.map_size = size
        self._tileimage_ = replika.assets.new_image((
            self.map_size[0] * self.tiles.cell_size[0],
            self.map_size[1] * self.tiles.cell_size[1]))
        self.tilemap = None
        self._update_tilemap_()

    def _update_tilemap_(self):
        self.tilemap = replika.ingame.new(self._tileimage_,
                                          self, 'map', position=(0, 0))
        
    def add_asset(self, asset, position=(0, 0), name='map'):
        if name == 'map':
            self.set_tile(position, asset)
            return self.tilemap
        return super(TileMap, self).add_asset(asset, position, name)

    def set_tile(self, position, tile_id):
        self._tileimage_ = replika.assets.paste_in(
            self._tileimage_,
            self.tiles[tile_id],
            position=(position[0] * self.tiles.cell_size[0],
                      position[1] * self.tiles.cell_size[1]))
        self._update_tilemap_()

    def update(self):
        self.tilemap.update()
        super(TileMap, self).update()
