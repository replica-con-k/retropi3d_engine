#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.assets
from replika.ingame import action

background = replika.assets.image('../assets/background.jpg')
woman = replika.assets.Loop(
    replika.assets.images(sorted(glob.glob('../assets/walk_*.png'))))

class Woman(replika.ingame.Puppet):
    def __init__(self, puppet_asset, layer, name, position=None,
                 distance=5.0):
        super(Woman, self).__init__(puppet_asset, layer, name,
                                    position, distance)


game = replika.new_game()
scene = game.new_scene(auto_switch=True)

scene.add_asset(background)

woman_graphics = replika.assets.Puppet({
    'initial': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_right': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_left': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')),
                              horizontal_flip=True))
})
woman_graphics.behaviour = Woman


test.start('Puppet() inherit test')


while game.is_running:
    position = (random.randint(-512, 512), random.randint(-384, 384))
    try:
        new_woman = scene.add_asset(woman_graphics, position=position)
        if not isinstance(new_woman, Woman):
            test.failed('Invalid type of InGame() object')            
    except:
        test.failed('Cannot inherit from Puppet() objects')
    if game.frame >= 50:
        game.quit()
    game.update()

test.ok()
