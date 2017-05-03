#!/usr/bin/env python
#

import test

import replika
import replika.assets

game = replika.new_game()
image = replika.assets.image('../assets/background.jpg')

test.start('Show image')

try:
    game.put_image(image)
except:
    test.failed('Cannot show image')

while game.is_running:
    game.update()
    if game.frame >= 50:
        game.quit()
    
test.ok()
