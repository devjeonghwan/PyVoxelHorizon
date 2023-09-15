from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes.wintypes as wintypes
import struct

class ClientContext:
    address                 : int               = None
    
    def __init__(self, address: int):
        self.address = address
    
    def get_function(self, offset, return_type, *argument_types, **keyword) -> ctypes.CFUNCTYPE:
        return ctypes.CFUNCTYPE(return_type, argument_types, keyword)(self.address + offset)

