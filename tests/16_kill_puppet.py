#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import glob

import test

import replika
import replika.assets

test.start('Kill puppet')
game = replika.new_game()
puppet = replika.assets.Puppet({
    'initial': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'final': replika.assets.Animation(
        replika.assets.load_tileset('../assets/explosion-sprite.png',
                                    grid_size=(5, 3)))
})

puppet = game.add_asset(puppet)
while (game.is_running):
    game.update()
    if game.frame >= 100:
        break
    if replika.key_state(1) or (game.frame == 50):
        try:
            puppet.kill()
        except Exception:
            test.failed('Cannot kill a puppet')

if not puppet.is_live:
    test.ok()

game.quit()
