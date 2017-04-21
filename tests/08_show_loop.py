#!/usr/bin/env python
#

import glob

import replika
import replika.assets

game = replika.new_game()
background = replika.assets.load_image('../assets/background.jpg')
game.put_image(background)

animation_frames = replika.assets.load_images(
    sorted(glob.glob('../assets/walk_*.png')))

test.start('Show loop animation')
try:
    game.put_animation(animation_frames, loop=True)
except:
    test.failed('Cannot show animation')
    
while game.is_running:
    game.update()
    if game.frame >= 100:
        game.quit()

test.ok()
