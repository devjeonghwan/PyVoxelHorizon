from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes
import ctypes.wintypes as wintypes
import struct

class SceneObject:
    def __init__(self, client_context, address):
        self.client_context = client_context
        self.address = address

        self.function_load_voxels = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPCWSTR)(self.client_context.address + SCENE_OFFSET['FUNCTION']['LOAD_VOXELS'])

    def load_voxels(self, file_path):
        self.function_load_voxels(self.address, file_path)

        # return self.client_context.address + SCENE_OFFSET['FUNCTION']['LOAD_VOXELS']