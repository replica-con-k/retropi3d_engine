#!/usr/bin/env python
#

import test

import replika
import replika.assets

background = replika.assets.image('../assets/background.jpg')
star = replika.assets.image('../assets/star.png')

game = replika.new_game()
scene = game.new_scene(auto_switch=True)

layer = scene.new_layer('foreground')

test.start('Draw in layers')

try:
    # Draw in default layer
    scene.add_asset(background)
    # Draw in the other layer
    layer.add_asset(star)
except:
    test.failed('Cannot draw in layers')

while game.is_running:
    if game.frame >= 100:
        game.quit()
    game.update()

test.ok()
