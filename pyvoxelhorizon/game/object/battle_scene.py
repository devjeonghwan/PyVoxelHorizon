from .client_context import *
from .voxel_object_manager import *
from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes
import ctypes.wintypes as wintypes
import struct

IS_FUNCTION_LOAD = False

FUNCTION_LOAD_VOXELS = None

def load_functions(client_context: ClientContext):
    global IS_FUNCTION_LOAD

    if IS_FUNCTION_LOAD:
        return

    IS_FUNCTION_LOAD = True

    global FUNCTION_LOAD_VOXELS
    FUNCTION_LOAD_VOXELS = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPCWSTR)(client_context.address + BATTLE_SCENE_OFFSET['FUNCTION']['LOAD_VOXELS'])

class BattleScene:
    client_context          : ClientContext     = None
    address                 : int               = None

    def __init__(self, client_context: ClientContext, address: int):
        self.client_context = client_context
        self.address = address
        
        load_functions(client_context)

    def get_voxel_object_manager(self) -> VoxelObjectManager:
        address = read_pointer_chain(self.address, [BATTLE_SCENE_OFFSET['FIELD']['VOXEL_OBJECT_MANAGER']])

        if address:
            return VoxelObjectManager(self.client_context, address)
        
        return None
    
    def load_voxels(self, file_path: str):
        FUNCTION_LOAD_VOXELS(self.address, file_path)