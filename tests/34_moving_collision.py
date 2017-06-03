#!/usr/bin/env python
#

import random

import test

import replika
import replika.layer
import replika.assets
import replika.ingame
import replika.physics

class Star(replika.ingame.Puppet):
    def __init__(self, puppet_asset, layer, name, position=None):
        super(Star, self).__init__(puppet_asset, layer, name, position, 5.0)
        self.direction = (random.randint(-5, 5), random.randint(-5, 5))
        
    def update(self):
        if ((self.body.x <= -512) or (self.body.x >= 512)):
            self.direction = (-self.direction[0], self.direction[1])
        elif ((self.body.y <= -384) or (self.body.y >= 384)):
            self.direction = (self.direction[0], -self.direction[1])            
        self.body.x += self.direction[0]
        self.body.y += self.direction[1]
        super(Star, self).update()

        
background = replika.assets.image('../assets/background.jpg')

star = replika.assets.Puppet({
    'initial': replika.assets.Loop(
        [replika.assets.image('../assets/star.png')])
    })
star.behaviour = Star

game = replika.new_game()
game.add_asset(background)
game.current_scene.new_layer('foreground',
                             layer_type=replika.layer.PhysicsLayer)
game.current_scene.set_default_layer('foreground')

test.start('Collision test')

def collision_handler(ingame_object):
    print 'Collision with %s' % ingame_object.name

for star_no in range(50):
    element = game.add_asset(star,
                             position=(random.randint(-512, 512),
                                       random.randint(-384, 384)),
                             name='star_%s' % star_no)
    element.collision = collision_handler
    element.body = replika.physics.create_body(
        replika.assets.image('../assets/star.png'))

try:
    while game.is_running:
        if replika.key_state(1) or (game.frame >= 5000):
            game.quit()
        game.update()
except:
    test.failed('Cannot detect collision with moving bodies')

test.ok()
