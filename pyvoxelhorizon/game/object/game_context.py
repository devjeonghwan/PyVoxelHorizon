from .client_context import *
from .battle_scene import *
from .key_code import *
from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes
import ctypes.wintypes as wintypes
import struct

IS_FUNCTION_LOAD = False

FUNCTION_WRITE_TEXT = None

def load_functions(client_context: ClientContext):
    global IS_FUNCTION_LOAD
    
    if IS_FUNCTION_LOAD:
        return

    IS_FUNCTION_LOAD = True

    global FUNCTION_WRITE_TEXT
    FUNCTION_WRITE_TEXT = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.ULONG, wintypes.LPCWSTR)(client_context.address + GAME_OFFSET['FUNCTION']['WRITE_TEXT'])

class GameContext:
    client_context          : ClientContext     = None
    address                 : int               = None

    def __init__(self, client_context: ClientContext, address: int):
        self.client_context = client_context
        self.address = address
        
        load_functions(client_context)

    def get_battle_scene(self) -> BattleScene:
        address = read_pointer_chain(self.address, [GAME_OFFSET['FIELD']['SCENE']])

        # Add to check scene is BattleScene

        if address:
            return BattleScene(self.client_context, address)
        
        return None

    def get_window_width(self) -> int:
        return read_memory(self.address + GAME_OFFSET['FIELD']['WINDOW_WIDTH'], ctypes.c_uint32)

    def get_window_height(self) -> int:
        return read_memory(self.address + GAME_OFFSET['FIELD']['WINDOW_HEIGHT'], ctypes.c_uint32)

    def get_device_width(self) -> int:
        return read_memory(self.address + GAME_OFFSET['FIELD']['DEVICE_WIDTH'], ctypes.c_uint32)

    def get_device_height(self) -> int:
        return read_memory(self.address + GAME_OFFSET['FIELD']['DEVICE_HEIGHT'], ctypes.c_uint32)

    def is_in_private_map(self) -> bool:
        return read_memory(self.address + GAME_OFFSET['FIELD']['IS_IN_PRIVATE_MAP'], ctypes.c_bool)

    def is_in_pvp_mode(self) -> bool:
        return read_memory(self.address + GAME_OFFSET['FIELD']['IS_IN_PVP_MODE'], ctypes.c_bool)

    def is_mouse_left_button_down(self) -> bool:
        return read_memory(self.address + GAME_OFFSET['FIELD']['MOUSE_LEFT_BUTTON_DOWN'], ctypes.c_bool)

    def is_mouse_middle_button_down(self) -> bool:
        return read_memory(self.address + GAME_OFFSET['FIELD']['MOUSE_MIDDLE_BUTTON_DOWN'], ctypes.c_bool)

    def is_mouse_right_button_down(self) -> bool:
        return read_memory(self.address + GAME_OFFSET['FIELD']['MOUSE_RIGHT_BUTTON_DOWN'], ctypes.c_bool)
    
    def is_key_press(self, virtual_key_code: KeyCode) -> bool:
        key_press_table_address = read_memory(self.address + GAME_OFFSET['FIELD']['KEY_PRESS_TABLE_ADDRESS'], ctypes.c_void_p)

        if not key_press_table_address:
            return False
        
        return read_memory(key_press_table_address + virtual_key_code.code, ctypes.c_ubyte) != 0
    
    def write_text_line(self, color: int, text: str):
        FUNCTION_WRITE_TEXT(self.address, color, text + "\n")
    
    def write_text(self, color: int, text: str):
        FUNCTION_WRITE_TEXT(self.address, color, text)

