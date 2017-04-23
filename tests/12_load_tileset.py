#!/usr/bin/env python
#

import test

import replika.assets

test.start('Load tileset')

try:
    tileset = replika.assets.load_tileset(
        '../assets/background.jpg',
        grid_size=(16, 12))
except:
    test.failed('Cannot load tileset')

test.ok()
