from .scene_object import SceneObject
from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes
import ctypes.wintypes as wintypes
import struct

class GameObject:
    def __init__(self, client_context, address):
        self.client_context = client_context
        self.address = address

    def get_scene(self):
        scene_address = read_pointer_chain(self.address, [GAME_OFFSET['FIELD']['SCENE']])

        if scene_address != 0:
            return SceneObject(self.client_context, scene_address)
        
        return None

    def get_window_width(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['WINDOW_WIDTH'], ctypes.c_uint32)

    def get_window_height(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['WINDOW_HEIGHT'], ctypes.c_uint32)

    def get_device_width(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['DEVICE_WIDTH'], ctypes.c_uint32)

    def get_device_height(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['DEVICE_HEIGHT'], ctypes.c_uint32)

    def is_in_private_map(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['IS_IN_PRIVATE_MAP'], ctypes.c_int32)

    def is_in_pvp_mode(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['IS_IN_PVP_MODE'], ctypes.c_int32)

    def is_mouse_left_button_down(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['MOUSE_LEFT_BUTTON_DOWN'], ctypes.c_int32)

    def is_mouse_middle_button_down(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['MOUSE_MIDDLE_BUTTON_DOWN'], ctypes.c_int32)

    def is_mouse_right_button_down(self):
        return read_memory(self.address + GAME_OFFSET['FIELD']['MOUSE_RIGHT_BUTTON_DOWN'], ctypes.c_int32)