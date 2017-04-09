#!/usr/bin/env python
#

import sys
sys.path.append('../')
import src as retropi3d
import src.sprites

RESOLUTION=(1024, 768)

world = retropi3d.sprites.World(RESOLUTION)
world.new_image(src.sprites.load('../assets/star.png'))

frames = 100
while world.loop_running():
    world.update()
    frames -= 1
    if frames < 0:
        break
world.destroy()
