#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import glob

import test

import replika
import replika.assets

K_LEFT = 105
K_RIGHT = 106
K_QUIT = 1

test.start('Move puppet')
game = replika.new_game()
move_right = replika.assets.load_images(
    sorted(glob.glob('../assets/walk_*.png')))
move_left = replika.assets.load_images(
    sorted(glob.glob('../assets/walk_*.png')), horizontal_flip=True)
explosion = replika.assets.load_tileset('../assets/explosion-sprite.png',
                                        grid_size=(5, 3))
puppet = game.spawn_puppet({
    'initial': move_right,
    'move_right': move_right,
    'move_left': move_left,
    'final': explosion
})

while game.is_running:
    game.update()
    if game.frame >= 200:
        break
    if replika.key_state(K_QUIT):
        puppet.kill()

    try:
        if replika.key_state(K_LEFT):
            puppet.set_state('move_left')

        if replika.key_state(K_RIGHT):
            puppet.set_state('move_right')
    except:
        test.failed('Cannot move puppet')

game.quit()
test.ok()
    
