#!/usr/bin/env python
#

import test

import glob
import random

import replika
import replika.assets

game = replika.new_game()
background = replika.assets.image('../assets/background.jpg')
game.put_image(background)

animation_frames = replika.assets.Loop(
    replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))
)

test.start('Show loop animation')
try:
    while game.is_running:
        position = (random.randint(-512, 512),
                    random.randint(-384, 384))
        game.put_animation(animation_frames, position)
        game.update()
        if game.frame >= 100:
            game.quit()
except:
    test.failed('Cannot show multiple animation loops')

test.ok()
