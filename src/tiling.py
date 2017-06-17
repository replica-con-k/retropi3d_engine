#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pi3d

import assets

class TileSet(object):
    '''
    TileSet is a kind of list of tiles grided in a image file
    '''
    def __init__(self, image_asset, grid_size, auto_resize=True):
        self.__image = image_asset.image
        self.__size = grid_size
        self.__cell_size = (image_asset.width / grid_size[0],
                            image_asset.height / grid_size[1])
        self.auto_resize = auto_resize

    @property
    def cell_size(self):
        if self.auto_resize:
            return self[0].image.size
        return self.__cell_size

    def __len__(self):
        return self.__size[0] * self.__size[1]

    def __iter__(self):
        return iter([self[e] for e in range(len(self))])
    
    def __getitem__(self, item):
        if item == -1:
            return self[len(self) - 1]
        if item not in range(len(self)):
            item %= len(self)
        tile_row = item / int(self.__size[0])
        tile_column = item - (tile_row * int(self.__size[0]))
        box_origin = (tile_column * self.__cell_size[0],
                      tile_row * self.__cell_size[1])
        box = (box_origin[0],
               box_origin[1],
               box_origin[0] + self.__cell_size[0],
               box_origin[1] + self.__cell_size[1])
        image = assets.Image(self.__image.crop(box))
        if self.auto_resize:
            image = assets.autoresize(image)
        return image
