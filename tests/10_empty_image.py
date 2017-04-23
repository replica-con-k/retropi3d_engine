#!/usr/bin/env python
#

import test

import glob
import random

import replika.assets


test.start('Empty image')
try:
    image = replika.assets.new_image((20, 20))
    print image
except:
    test.failed('Cannot create empty image')

test.ok()
