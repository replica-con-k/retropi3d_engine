#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import pi3d

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
