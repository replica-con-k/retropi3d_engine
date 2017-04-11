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
world.new_image(src.sprites.load('../assets/background.jpg'))

frames = 200
frame_files = sorted(glob.glob('../assets/walk_*.png'))

while world.loop_running():
    world.new_animation(
        [src.sprites.load(f, True) for f in frame_files],
        (random.randint(-512, 512), random.randint(-384, 384)),
        fps=20,
        loop=True)
    world.new_animation(
        [src.sprites.load(f, False) for f in frame_files],
        (random.randint(-512, 512), random.randint(-384, 384)),
        fps=20,
        loop=True)
    world.update()
    frames -= 1
    if frames < 0:
        break
world.destroy()
