#!/usr/bin/env python
#

import test

import replika
import replika.assets

import random

game = replika.new_game()
tileset = replika.assets.load_tileset('../assets/tileset.png',
                                      grid_size=(16, 12))
test.start('Draw tiles')

try:
    while game.is_running:
        tile = random.randint(0, len(tileset))
        game.add_asset(tileset[tile],
                       position=(random.randint(-512, 512),
                                 random.randint(-384, 384)))
        game.update()
        if game.frame >= 100:
            game.quit()
            
except:
    test.failed('Cannot draw tiles')

test.ok()
