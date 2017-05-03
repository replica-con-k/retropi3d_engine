#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pi3d
import PIL

import tiling

WIDTHS = [4, 8, 16, 32, 48, 64, 72, 96, 128, 144, 192, 256,
          288, 384, 512, 576, 640, 720, 768, 800, 960, 1024, 1080, 1920]

class Image(object):
    def __init__(self, image, image_file=None, position=None):
        self.image = image
        self.image_file = image_file
        self.position = position

    @property
    def width(self):
        return self.image.width

    @property
    def height(self):
        return self.image.height

    @property
    def size(self):
        return (self.width, self.height)

    @property
    def texture(self):
        return pi3d.Texture(self.image, blend=False)


class Animation(object):
    def __init__(self, images, position=None, fps=None):
        self.images = images
        self.position = position
        self.fps = fps
        
    @property
    def textures(self):
        return [image.texture for image in self.images]

    @property
    def first_frame(self):
        return self.images[0]

    @property
    def as_loop(self):
        return Loop(self.images, self.position, self.fps)


class Loop(Animation):
    def __init__(self, images, position=None, fps=None):
        super(Loop, self).__init__(images, position, fps)


class Puppet(object):
    def __init__(self, animations, position=None):
        assert(isinstance(animations, dict))
        assert('initial' in animations.keys())
        self.animations = animations
        self.position = position

    @property
    def actions(self):
        return self.animations.keys()

    def __getitem__(self, item):
        return self.animations[item]

    
def image(image_file, horizontal_flip=False, vertical_flip=False,
          auto_resize=True):
    '''
    Load single image file, return a Texture() object
    '''        
    image = PIL.Image.open(image_file).convert('RGBA')
    if horizontal_flip:
        image = image.transpose(PIL.Image.FLIP_LEFT_RIGHT)
    if vertical_flip:
        image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
    image = Image(image, image_file)
    if auto_resize:
        image = autoresize(image)
    return image


def images(image_files, horizontal_flip=False, vertical_flip=False,
           auto_resize=True):
    '''
    Load one or more images, return single or list Texture() objects
    '''
    return [
        image(
            image_file, horizontal_flip, vertical_flip, auto_resize
        ) for image_file in image_files
    ]
    

def autoresize(asset, mode=PIL.Image.LANCZOS):
    if isinstance(asset, Image):
        image = asset.image
        # work out if sizes > MAX_SIZE or coerce to golden values in WIDTHS
        if image.height > image.width and image.height > WIDTHS[-1]:
            image = image.resize(
                (int((WIDTHS[-1] * image.width) / image.height), WIDTHS[-1]),
                resample=PIL.Image.LANCZOS)
        n = len(WIDTHS)
        for i in xrange(n-1, 0, -1):
            if image.width == WIDTHS[i]:
                break # Image has a nice size
            if image.width > WIDTHS[i]:
                image = image.resize(
                    (WIDTHS[i], int((WIDTHS[i] * image.height) / image.width)),
                    resample=PIL.Image.LANCZOS)
                break
        return Image(image)

def new_image(size):
    '''
    Create empty RGBA image
    '''
    return Image(PIL.Image.new('RGBA', size))


def paste_in(destination, source, position=(0, 0)):
    '''
    Paste source image into destination image at given position
    '''
    destination = destination.image.copy()
    destination.paste(source.image, position, mask=source.image)
    return Image(destination)


def load_tileset(image_file, grid_size):
    '''
    Load a grid_size set of tiles, loaded from image_file
    '''
    return tiling.TileSet(image(image_file), grid_size)
