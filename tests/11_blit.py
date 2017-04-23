#!/usr/bin/env python
#

import test

import glob
import random

import replika.assets

game = replika.new_game()

star = replika.assets.load_image('../assets/star.png')
size = (star.ix * 2, star.iy * 2)

image = replika.assets.new_image(size)

test.start('Blit image')
try:
    image = replika.assets.paste_in(image, star, position=(-10, -10))
    image = replika.assets.paste_in(image, star, position=(10, 10))
    game.put_image(image)
    while game.is_running:
        game.update()
        if game.frame >= 100:
            game.quit()   
except:
    test.failed('Cannot blit images')

test.ok()
