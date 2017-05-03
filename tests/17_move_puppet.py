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
puppet = game.spawn_puppet(replika.assets.Puppet({
    'initial': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_right': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_left': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')),
                              horizontal_flip=True))
}))

while game.is_running:
    game.update()
    if game.frame >= 100:
        break
    try:
        if replika.key_state(K_LEFT):
            puppet.set_state('move_left')
        if replika.key_state(K_RIGHT):
            puppet.set_state('move_right')
        if replika.key_state(K_QUIT):
            puppet.kill()
    except:
        test.failed('Cannot move puppet')

game.quit()
test.ok()
    
