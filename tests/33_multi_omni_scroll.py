#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.layer
import replika.assets

background_image = replika.assets.image('../assets/continuous_background.jpg')
ghosts = replika.assets.image('../assets/ghostly_gouls.png')

game = replika.new_game()
scene = game.new_scene(auto_switch=True)

test.start('Multiple omni scroll layer test')
try:
    background = scene.new_layer(layer_type=replika.layer.Scroll)
    foreground = scene.new_layer(layer_type=replika.layer.Scroll)
    background.add_asset(background_image)
    foreground.add_asset(ghosts)
    scroll = [background, foreground]
except:
    test.failed('Cannot create multiple Scroll layers')

def move(scroll, offset, speed_factor=2.5):
    plane_speed = 1.0
    for plane in scroll:
        plane.move((offset[0] * plane_speed, offset[1] * plane_speed))
        plane_speed *= speed_factor

while game.is_running:
    if replika.key_state(105):
        move(scroll, (-10, 0))
    if replika.key_state(106):
        move(scroll, (10, 0))
    if replika.key_state(103):
        move(scroll, (0, 10))
    if replika.key_state(108):
        move(scroll, (0, -10))
    if (game.frame > 1000) or replika.key_state(1):
        game.quit()
    game.update()

test.ok()
