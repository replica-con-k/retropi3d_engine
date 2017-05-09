#!/usr/bin/env python
#

import test

import replika
import replika.assets

game = replika.new_game(do_input=False)
animation = replika.assets.Loop(
    replika.assets.load_tileset('../assets/explosion-sprite.png',
                                grid_size=(5, 3)))
    
test.start('Animate tiles')

try:
    game.add_asset(animation)
except:
    test.failed('Cannot animate tiles')
    
while game.is_running:
    game.update()
    if game.frame >= 50:
        game.quit()

test.ok()
