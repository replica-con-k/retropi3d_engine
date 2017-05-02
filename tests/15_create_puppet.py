#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import glob

import test

import replika
import replika.assets

test.start('New puppet')
game = replika.new_game()

try:
    puppet = game.spawn_puppet({
        'initial': replika.assets.load_images(
            sorted(glob.glob('../assets/walk_*.png')))
    })
except Exception:
    test.failed('Cannot instance a puppet')

while game.is_running:
    game.update()
    if game.frame >= 100:
        game.quit()
    if replika.key_state(1):
        puppet.kill()

test.ok()
