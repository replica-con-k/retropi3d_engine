#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.assets


background = replika.assets.image('../assets/background.jpg')
star = replika.assets.image('../assets/star.png')
woman = replika.assets.Loop(
    replika.assets.images(sorted(glob.glob('../assets/walk_*.png'))))

game = replika.new_game()
game.put_image(background)

test.start('Move elements')

image = game.put_image(star, (random.randint(-512, 512),
                              random.randint(-300, 300)))

animation = game.put_animation(woman, (random.randint(-512, 512),
                                       random.randint(-300, 300)))

puppet = game.spawn_puppet(replika.assets.Puppet({
    'initial': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_right': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_left': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')),
                              horizontal_flip=True))
}), (random.randint(-512, 512), random.randint(-300, 300)))


x_image = image.body.x
image_dir = 10

x_animation = animation.body.x
animation_dir = -10

x_puppet = puppet.body.x
puppet.set_state('move_right')
puppet_dir = 10

while game.is_running:
    x_image += image_dir
    if (x_image <= -512) or (x_image >= 512):
        image_dir = -image_dir
    x_animation += animation_dir
    if (x_animation <= -512) or (x_animation >= 512):
        animation_dir = -animation_dir
    x_puppet += puppet_dir
    if (x_puppet <= -512) or (x_puppet >= 512):
        puppet_dir = -puppet_dir
        if puppet_dir > 0:
            puppet.set_state('move_right')
        else:
            puppet.set_state('move_left')
    try:
        image.body.x = x_image
        animation.body.x = x_animation
        puppet.body.x = x_puppet
    except:
        test.failed('Cannot draw multiple images')
    if game.frame >= 100:
        game.quit()
    game.update()

test.ok()
