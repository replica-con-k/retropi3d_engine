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

test.start('Scroll layer test')
try:
    scroll = scene.new_layer(layer_type=replika.layer.HorizontalScroll)
except:
    test.failed('Cannot create HorizontalScroll() layer')
scroll.add_asset(background)

while game.is_running:
    if replika.key_state(105):
        scroll.move((-10, 0))
    if replika.key_state(106):
        scroll.move((10, 0))
    if replika.key_state(103):
        scroll.move((0, -10))
    if replika.key_state(108):
        scroll.move((0, 10))
    if replika.mouse_buttons()[0]:
        scroll.move(replika.mouse_position())        
    if (game.frame > 100) or replika.key_state(1):
        game.quit()
    game.update()

test.ok()
