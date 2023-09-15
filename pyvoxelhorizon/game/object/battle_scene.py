from .client_context import *
from .voxel_object_manager import *
from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes
import ctypes.wintypes as wintypes
import struct

class BattleScene:
    client_context          : ClientContext     = None
    address                 : int               = None

    function_load_voxels    : ctypes.CFUNCTYPE  = None
    
    def __init__(self, client_context: ClientContext, address: int):
        self.client_context = client_context
        self.address = address

        self.function_load_voxels = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPCWSTR)(self.client_context.address + BATTLE_SCENE_OFFSET['FUNCTION']['LOAD_VOXELS'])

    def get_voxel_object_manager(self) -> VoxelObjectManager:
        address = read_pointer_chain(self.address, [BATTLE_SCENE_OFFSET['FIELD']['VOXEL_OBJECT_MANAGER']])

        if address:
            return VoxelObjectManager(self.client_context, address)
        
        return None
    
    def load_voxels(self, file_path: str):
        self.function_load_voxels(self.address, file_path)

        # return self.client_context.address + SCENE_OFFSET['FUNCTION']['LOAD_VOXELS']