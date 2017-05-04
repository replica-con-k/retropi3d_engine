#!/usr/bin/env python
#

import random

import test

import replika
import replika.assets
import replika.physics


background = replika.assets.image('../assets/background.jpg')
star = replika.assets.image('../assets/star.png')

game = replika.new_game()
game.put_image(background)

test.start('Collision test')

def collision_handler(ingame_object):
    print 'Collision with %s' % ingame_object.name

try:
    star_no = 0
    while game.is_running:
        element = game.put_image(star,
                                 (random.randint(-512, 512),
                                  random.randint(-384, 384)),
                                 name='star_%s' % star_no)
        element.collision = collision_handler
        element.body = replika.physics.create_body(star)
        game.update()
        if game.frame >= 50:
            game.quit()
        star_no += 1
except:
    test.failed('Cannot draw multiple images')

test.ok()
