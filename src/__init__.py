#!/usr/bin/env python
#

import uuid
import collections
import traceback

import pi3d

import ingame

_DEFAULT_RESOLUTION_ = (1024, 768)
_DEFAULT_FPS_ = 20
_DEFAULT_SHADER_ = 'uv_flat'


class _No_input_(object):
    def do_input_events(self):
        pass
_INPUTS_ = _No_input_()
_KEYBOARD_ = {}

K_ESC = 1


def key_state(key):
    return _KEYBOARD_.get(key, False)


class Game(object):
    def __init__(self, resolution, fps):
        width, height = resolution
        self.display = pi3d.Display.create(w=width, h=height,
                                           frames_per_second=fps)
        self.camera = pi3d.Camera(is_3d=False)
        self.shader = pi3d.Shader(_DEFAULT_SHADER_)
        self.elements = collections.OrderedDict()
        self._frame = 0

    @property
    def frame(self):
        return self._frame

    def put_image(self, image, initial_position=(0, 0), name=None):
        name = name or str(uuid.uuid4())
        self.elements[name] = ingame.Image(image, self, name,
                                           initial_position)
        return self.elements[name]
    
    @property
    def is_running(self):
        if self.display is None:
            return False
        return self.display.loop_running()

    def quit(self):
        if self.display is None:
            return
        self.display.destroy()
        self.display = None
        self.elements = collections.OrderedDict()

    def __del__(self):
        self.quit()

    def update(self):
        self._frame += 1
        _INPUTS_.do_input_events()
        for element in reversed(self.elements.values()):
            element.update()


def _keyboard_handler_(sourceType, sourceIndex, key, value):
    global _KEYBOARD_
    if sourceType != 'keyboard':
        return
    _KEYBOARD_[key] = (value == 1)
    print sourceType, sourceIndex, key, value


def new_game(resolution=_DEFAULT_RESOLUTION_, fps=_DEFAULT_FPS_):
    global _INPUTS_
    if isinstance(_INPUTS_, _No_input_):
        _INPUTS_ = pi3d.event.Event.InputEvents(_keyboard_handler_)
    return Game(resolution, fps)
