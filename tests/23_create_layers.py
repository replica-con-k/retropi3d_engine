#!/usr/bin/env python
#

import test

import replika
import replika.assets

game = replika.new_game()
scene = game.new_scene()

test.start('Create layers')

try:
    layer1 = scene.new_layer()
    layer2 = scene.new_layer()
except:
    test.failed('Cannot create layer')

game.quit()    
test.ok()
