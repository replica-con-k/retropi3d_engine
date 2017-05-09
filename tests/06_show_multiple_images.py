#!/usr/bin/env python
#

import random

import test

import replika
import replika.assets


background = replika.assets.image('../assets/background.jpg')
star = replika.assets.image('../assets/star.png')

game = replika.new_game()
game.add_asset(background)

test.start('Show multiple images')

try:
    while game.is_running:
        game.add_asset(star, (random.randint(-512, 512),
                              random.randint(-384, 384)))
        game.update()
        if game.frame >= 50:
            game.quit()
except:
    test.failed('Cannot draw multiple images')

test.ok()
