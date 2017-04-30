#!/usr/bin/env python
#

import test

import replika
import replika.assets

game = replika.new_game()
image1 = replika.assets.load_image('../assets/background.jpg')
image2 = replika.assets.load_image('../assets/background.jpg',
                                   horizontal_flip=True)
game.put_image(image1)

scene2 = game.new_scene()
scene2.put_image(image2)

test.start('Switch scenes')

while game.is_running:
    game.update()
    if game.frame >= 100:
        game.quit()
    if game.frame == 50:
        try:
            game.switch_scene(scene2)
        except:
            test.failed('Cannot switch scene')
    
test.ok()
