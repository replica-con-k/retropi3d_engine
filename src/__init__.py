#!/usr/bin/env python
#

import uuid
import collections
import traceback

import pi3d

import replika.ingame
import replika.physics

try:
    import pymunk
    _USE_PYMUNK_ = True
except ImportError:
    _USE_PYMUNK_ = False

_DEFAULT_RESOLUTION_ = (1024, 768)
_DEFAULT_FPS_ = 20
_DEFAULT_SHADER_ = 'uv_flat'


class _No_input_(object):
    def do_input_events(self):
        pass

class _No_mouse_(object):
    def position(self):
        return (0, 0)

_INPUTS_ = _No_input_()
_MOUSE_ = _No_mouse_()
_KEYBOARD_ = {}
_MOUSE_POSITION_ = (0, 0)
_MOUSE_LEFT_BUTTON_ = False
_MOUSE_RIGHT_BUTTON_ = False

K_ESC = 1


def key_state(key):
    return _KEYBOARD_.get(key, False)

def mouse_position():
    return _MOUSE_POSITION_

def mouse_buttons():
    return _MOUSE_LEFT_BUTTON_, _MOUSE_RIGHT_BUTTON_

class Game(object):
    def __init__(self, resolution, fps):
        width, height = resolution
        self.display = pi3d.Display.create(w=width, h=height,
                                           frames_per_second=fps)
        self.camera = pi3d.Camera(is_3d=False)
        self.shader = pi3d.Shader(_DEFAULT_SHADER_)
        self.scenes = collections.OrderedDict()
        self._frame = 0
        self._fps = fps

        self.new_scene('initial')
        self.__current_scene = 'initial'

    def new_scene(self, name=None, auto_switch=False):
        name = name or str(uuid.uuid4())
        scene = ingame.Scene(self, name)
        self.scenes[name] = scene
        if auto_switch:
            self.switch_scene(scene)
        return scene
        
    @property
    def current_scene(self):
        return self.scenes[self.__current_scene]

    def switch_scene(self, scene):
        if isinstance(scene, ingame.Scene):
            scene = scene.name
        if scene not in self.scenes.keys():
            return False
        self.__current_scene = scene
        return True
    
    @property
    def frame(self):
        return self._frame

    @property
    def fps(self):
        return self._fps

    def add_asset(self, asset, position=(0, 0), name=None):
        return self.current_scene.add_asset(asset, position, name)
                          
    @property
    def is_running(self):
        if self.display is None:
            return False
        return self.display.loop_running()

    def quit(self):
        if self.display is None:
            return
        self.current_scene.quit()
        self.display.destroy()
        self.display = None

    def __del__(self):
        self.quit()

    def update(self):
        self._frame += 1
        _INPUTS_.do_input_events()
        self.current_scene.update()


def _keyboard_handler_(sourceType, sourceIndex, key, value):
    global _KEYBOARD_
    global _MOUSE_LEFT_BUTTON_    
    global _MOUSE_RIGHT_BUTTON_
    if sourceType != 'keyboard':
        return
    if sourceIndex == 4:
        if key == 272:
            _MOUSE_LEFT_BUTTON_ = value == 1
        if key == 273:
            _MOUSE_RIGHT_BUTTON_ = value == 1
    _KEYBOARD_[key] = ((value == 1) or (value == 2))
    print sourceType, sourceIndex, key, value


def _mouse_handler_(sourceType, sourceIndex, x, y, v, h):
    global _MOUSE_POSITION_
    _MOUSE_POSITION_ = (_MOUSE_POSITION_[0] + x, _MOUSE_POSITION_[1] + y)


def new_game(resolution=_DEFAULT_RESOLUTION_, fps=_DEFAULT_FPS_,
             do_input=True):
    global _INPUTS_
    game = Game(resolution, fps)
    if isinstance(_INPUTS_, _No_input_) and do_input:
        _INPUTS_ = pi3d.event.Event.InputEvents(_keyboard_handler_,
                                                _mouse_handler_)
    return game
