#!/usr/bin/env python
#

import test

import glob

import replika
import replika.assets

game = replika.new_game()
background = replika.assets.image('../assets/background.jpg')
game.add_asset(background)

animation = replika.assets.Loop(
    replika.assets.images([
        '../assets/continuous_background.jpg',
        '../assets/continuous_background_opa75.png',
        '../assets/continuous_background_opa50.png',
        '../assets/continuous_background_opa25.png',
        '../assets/continuous_background_opa10.png',
        '../assets/continuous_background_opa25.png',
        '../assets/continuous_background_opa50.png',
        '../assets/continuous_background_opa75.png'
    ])
)
animation.fps = 10

test.start('Show loop animation with different alpha values')
try:
    game.add_asset(animation)
except:
    test.failed('Cannot show animation')
    
while game.is_running:
    game.update()
    if game.frame >= 75:
        game.quit()

test.ok()
