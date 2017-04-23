#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pi3d
import PIL

import tiling

def load_image(image_file, horizontal_flip=False, vertical_flip=False):
    '''
    Load single image file, return a Texture() object
    '''
    flip = 1 if vertical_flip else 0
    flip += 2 if horizontal_flip else 0
    return pi3d.Texture(image_file, blend=False, flip=flip)

def load_images(image_files, horizontal_flip=False, vertical_flip=False):
    '''
    Load one or more images, return single or list Texture() objects
    '''
    return [
        load_image(
            image, horizontal_flip, vertical_flip) for image in image_files
    ]

def new_image(size):
    '''
    Create empty RGBA image
    '''
    return pi3d.Texture(PIL.Image.new('RGBA', size))

def paste_in(destination, source, position=(0, 0)):
    '''
    Paste source imagen into destination image at give position
    '''
    region = (position[0], position[1],
              position[0] + source.ix, position[1] + source.iy)
    destination = PIL.Image.fromarray(destination.image, 'RGBA')
    source = PIL.Image.fromarray(source.image, 'RGBA')
    destination.paste(source, position, mask=source)
    return pi3d.Texture(destination)

def load_tileset(image_file, grid_size):
    '''
    Load a grid_size set of tiles, loaded from image_file
    '''
    return tiling.TileSet(load_image(image_file), grid_size)
