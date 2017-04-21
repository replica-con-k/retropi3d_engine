#!/usr/bin/env python
#

import random

import test

import replika
import replika.assets


background = replika.assets.load_image('../assets/background.jpg')
star = replika.assets.load_image('../assets/star.png')

game = replika.new_game()
game.put_image(background)

test.start('Show multiple images')

try:
    while game.is_running:
        game.put_image(star,
                       (random.randint(-512, 512),
                        random.randint(-384, 384)))
        game.update()
        if game.frame >= 100:
            game.quit()
except:
    test.failed('Cannot draw multiple images')

test.ok()
