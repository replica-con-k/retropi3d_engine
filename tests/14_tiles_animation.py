#!/usr/bin/env python
#

import test

import replika
import replika.assets

game = replika.new_game(do_input=False)
tileset = replika.assets.load_tileset('../assets/explosion-sprite.png',
                                      grid_size=(5, 3))
    
test.start('Animate tiles')

try:
    game.put_animation(tileset, loop=True)
except:
    test.failed('Cannot animate tiles')
    
while game.is_running:
    game.update()
    if game.frame >= 100:
        game.quit()

test.ok()
