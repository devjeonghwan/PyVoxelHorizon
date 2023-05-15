from .game_object import GameObject
from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes
import ctypes.wintypes as wintypes
import struct

class ClientContext:
    def __init__(self, address):
        self.address = address

    def get_game(self):
        game_address = read_pointer_chain(self.address, [GLOBAL_OFFSET['STATIC']['GAME']])

        if game_address != 0:
            return GameObject(self, game_address)
        
        return None