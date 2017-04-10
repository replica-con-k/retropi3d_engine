#!/usr/bin/env python
#

import sys
sys.path.append('../')
import src as retropi3d
import src.sprites

import random

RESOLUTION=(1024, 768)

world = retropi3d.sprites.World(RESOLUTION)
world.new_image(src.sprites.load('../assets/background.jpg'))

frames = 100
while world.loop_running():
    world.new_image(src.sprites.load('../assets/star.png'),
                    (random.randint(-512, 512), random.randint(-384, 384)))
    world.update()
    frames -= 1
    if frames < 0:
        break
world.destroy()
