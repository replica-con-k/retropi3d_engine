#!/usr/bin/env python
#

import test

import replika.assets

test.start('Load image')

try:
    image = replika.assets.image('../assets/background.jpg')
except:
    test.failed('Cannot load image')

test.ok()
