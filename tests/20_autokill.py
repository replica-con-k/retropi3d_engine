#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import glob
import random

import test

import replika
import replika.assets

game = replika.new_game()
explosion = replika.assets.load_tileset('../assets/explosion-sprite.png',
                                        grid_size=(5, 3))
test.start('Auto kill animations')

while (game.is_running):
    position = (random.randint(-512, 512),
                random.randint(-384, 384))
    try:
        game.put_animation(explosion, position)
    except:
        test.failed('Cannot put auto-kill animation')
    game.update()
    if game.frame >= 100:
        break

game.quit()
test.ok()
