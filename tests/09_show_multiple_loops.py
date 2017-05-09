#!/usr/bin/env python
#

import test

import glob
import random

import replika
import replika.assets

game = replika.new_game()
background = replika.assets.image('../assets/background.jpg')
game.add_asset(background)

animation_frames = replika.assets.Loop(
    replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))
)

test.start('Show loop animation')
try:
    while game.is_running:
        game.add_asset(animation_frames,
                       position=(random.randint(-512, 512),
                                 random.randint(-384, 384)))
        game.update()
        if game.frame >= 100:
            game.quit()
except:
    test.failed('Cannot show multiple animation loops')

test.ok()
