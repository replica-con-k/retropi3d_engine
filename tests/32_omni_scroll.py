#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.layer
import replika.assets

background_image = replika.assets.image('../assets/continuous_background.jpg')

game = replika.new_game()
scene = game.new_scene(auto_switch=True)

test.start('Omni scroll layer test')
try:
    background = scene.new_layer(layer_type=replika.layer.Scroll)
    background.add_asset(background_image)
except:
    test.failed('Cannot create Scroll layer')

while game.is_running:
    if replika.key_state(105):
        background.move((-10, 0))
    if replika.key_state(106):
        background.move((10, 0))
    if replika.key_state(103):
        background.move((0, 10))
    if replika.key_state(108):
        background.move((0, -10))
    if (game.frame > 1000) or replika.key_state(1):
        game.quit()
    game.update()

test.ok()
