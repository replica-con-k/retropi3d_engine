#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pi3d
import PIL


class TileSet(object):
    '''
    TileSet is a kind of list of tiles grided in a image file
    '''
    def __init__(self, texture, grid_size):
        self.__image = PIL.Image.fromarray(texture.image)
        self.__size = grid_size
        self.__cell_size = (texture.ix / grid_size[0],
                            texture.iy / grid_size[1])

    def __len__(self):
        return self.__size[0] * self.__size[1]

    def __iter__(self):
        return iter([self[e] for e in range(len(self))])
    
    def __getitem__(self, item):
        if item == -1:
            return self[len(self) - 1]
        if item not in range(len(self)):
            raise ValueError
        tile_row = item / int(self.__size[0])
        tile_column = item - (tile_row * int(self.__size[0]))
        box_origin = (tile_column * self.__cell_size[0],
                      tile_row * self.__cell_size[1])
        box = (box_origin[0],
               box_origin[1],
               box_origin[0] + self.__cell_size[0],
               box_origin[1] + self.__cell_size[1])
        return pi3d.Texture(self.__image.crop(box))
