#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.layer
import replika.assets

background = replika.assets.image('../assets/parallax_05.png')
game = replika.new_game((background.size[0] * 2, background.size[1]))
scene = game.new_scene(auto_switch=True)

background_planes = []
for plane_image in reversed(sorted(glob.glob('../assets/parallax_*.png'))):
    plane = scene.new_layer(layer_type=replika.layer.HorizontalScroll)
    plane.add_asset(replika.assets.image(plane_image))
    background_planes.append(plane)

test.start('Parallax scroll test')

while game.is_running:
    speed_factor = 1.0
    for plane in background_planes:
        plane.move((int(-3.0 * speed_factor), 0))
        speed_factor *= 1.4
    if (game.frame > 100) or replika.key_state(1):
        game.quit()
    game.update()

test.ok()
