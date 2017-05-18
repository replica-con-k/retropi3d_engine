#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.layer
import replika.assets

bottom = replika.assets.image('../assets/parallax_01.png')
background = replika.assets.image('../assets/background.jpg')

game = replika.new_game(background.size)
scene = game.new_scene(auto_switch=True)

test.start('Multi scroll layer test')
try:
    vertical = scene.new_layer(layer_type=replika.layer.VerticalScroll)
    ground = scene.new_layer(layer_type=replika.layer.HorizontalScroll)
    ground.add_asset(bottom)
    vertical.add_asset(background)
except:
    test.failed('Cannot create several scroll layers')

while game.is_running:
    if replika.key_state(105):
        ground.move((-10, 0))
    if replika.key_state(106):
        ground.move((10, 0))
    if replika.key_state(103):
        vertical.move((0, -10))
    if replika.key_state(108):
        vertical.move((0, 10))
    if (game.frame > 1000) or replika.key_state(1):
        game.quit()
    game.update()

test.ok()
