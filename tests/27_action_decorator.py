#!/usr/bin/env python
#

import glob
import random

import test

import replika
import replika.assets
from replika.ingame import action

background = replika.assets.image('../assets/background.jpg')


class Woman(replika.ingame.Puppet):
    def __init__(self, puppet_asset, layer, name, position=None,
                 distance=5.0):
        super(Woman, self).__init__(puppet_asset, layer, name,
                                    position, distance)
        self.__current_action = self.initial

    def initial(self):
        if self.current_animation.is_finished:
            self.__current_action = self.move_right
    
    def update(self):
        self.__current_action()
        super(Woman, self).update()

    @action
    def move_right(self):
        self.body.x += 10
        if self.body.x >= 512:
            self.__current_action = self.move_left

    @action
    def move_left(self):
        self.body.x -= 10
        if self.body.x <= -512:
            self.__current_action = self.move_right


woman_puppet = replika.assets.Puppet({
    'initial': replika.assets.Animation(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_right': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')))),
    'move_left': replika.assets.Loop(
        replika.assets.images(sorted(glob.glob('../assets/walk_*.png')),
                              horizontal_flip=True))
})
woman_puppet.behaviour = Woman

game = replika.new_game()
scene = game.new_scene(auto_switch=True)

scene.add_asset(background)
test.start('"action" decorator test')

while game.is_running:
    position = (random.randint(-512, 512), random.randint(-384, 384))
    try:
        scene.add_asset(woman_puppet, position=position)
    except:
        test.failed('"action" decorator test failed')
    if game.frame >= 50:
        game.quit()
    game.update()

test.ok()
