#!/usr/bin/env python
#

import test

import replika
import replika.assets

game = replika.new_game()
image = replika.assets.load_image('../assets/background.jpg')


test.start('Create scenes')

try:
    scene1 = game.current_scene
    scene2 = game.new_scene()
except:
    test.failed('Cannot create additional scene')

while game.is_running:
    game.update()
    if game.frame >= 50:
        game.quit()
    
test.ok()
