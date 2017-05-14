#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.assets
from replika.ingame import action

background = replika.assets.image('../assets/scroll.png')
game = replika.new_game()
scene = game.new_scene(auto_switch=True)

background = scene.add_asset(background)

test.start('"action" decorator test')

while game.is_running:
    mouse_position = replika.mouse_position()
    background.body.position = (background.body.position[0], -mouse_position[1])
    if (game.frame > 100) or replika.mouse_buttons()[0]:
        game.quit()
    game.update()

test.ok()
