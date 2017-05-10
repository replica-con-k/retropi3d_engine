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

scene.add_asset(background)
scene.add_asset(star, layer='foreground')

test.start('Scroll layers')

x_ofs = 0
while game.is_running:
    if game.frame >= 100:
        game.quit()
    try:
        scene.default_layer.offset = (x_ofs, 0)
        layer.offset = (-x_ofs, 0)
    except:
        test.failed('Cannot draw in layers')
    x_ofs += 1
    game.update()

test.ok()
