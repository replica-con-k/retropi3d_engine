#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

import test

import replika

test.start('New game')

try:
    game = replika.new_game()
    game.quit()
except Exception:
    test.failed('Cannot instance new game')

test.ok()
