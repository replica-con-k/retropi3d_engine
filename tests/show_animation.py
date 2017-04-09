#!/usr/bin/env python
#

import sys
import glob

sys.path.append('../')
import src as retropi3d
import src.sprites

import random

RESOLUTION=(1024, 768)

world = retropi3d.sprites.World(RESOLUTION)

frames = 100
while world.loop_running():
    world.new_animation(
        [src.sprites.load(f) for f in glob.glob('../assets/walk_*.png')],
        (random.randint(-512, 512), random.randint(-384, 384)),
        loop=True)
    world.update()
    frames -= 1
    if frames < 0:
        break
world.destroy()
