#!/usr/bin/env python
#

import test

import random

import replika
import replika.layer
import replika.assets

tileset = replika.assets.load_tileset('../assets/tileset.png',
                                      grid_size=(16, 12))
game = replika.new_game()
scene = game.new_scene(auto_switch=True)
test.start('TileMap layer creation')

map_size = (100, 20)

layer = replika.layer.TileMap(tileset, size=map_size, scene=scene)
scene.layers[layer.name] = layer
scene.set_default_layer(layer)

while game.is_running:
    try:
        layer.set_tile((random.randint(0, map_size[0]),
                        random.randint(0, map_size[1])),
                       random.randint(0, len(tileset)))
    except:
        test.failed('Cannot draw in tiles in a tilemap')
    if game.frame >= 100:
        game.quit()
    game.update()

test.ok()
