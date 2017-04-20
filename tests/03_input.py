#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import test

import replika

test.start('Show input events')

game = replika.new_game()
try:
    print('Running the test, print ESC to quit...')
    while game.is_running:
        game.update()
        if replika.key_state(1):
            game.quit()
except Exception:
    test.failed('Cannot get input events')
test.ok()
