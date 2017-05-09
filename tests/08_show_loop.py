#!/usr/bin/env python
#

import test

import glob

import replika
import replika.assets

game = replika.new_game()
background = replika.assets.image('../assets/background.jpg')
game.add_asset(background)

animation = replika.assets.Loop(
    replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))
)

test.start('Show loop animation')
try:
    game.add_asset(animation)
except:
    test.failed('Cannot show animation')
    
while game.is_running:
    game.update()
    if game.frame >= 50:
        game.quit()

test.ok()
