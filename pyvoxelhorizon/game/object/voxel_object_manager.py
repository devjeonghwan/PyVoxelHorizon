from .client_context import *
from .voxel_object import *
from .vector3 import *

from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

import ctypes
import ctypes.wintypes as wintypes
import struct

VOXEL_OBJECT_SIZE = 400
VOXEL_OBJECT_HALF_SIZE = int(400 / 2)

def align_coord_to_voxel_object(value: float):
    if value >= 0:
        return int(value / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE + VOXEL_OBJECT_HALF_SIZE
    else:
        return int((value + 1) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE - VOXEL_OBJECT_HALF_SIZE

def align_vector3_to_voxel_object(vector: Vector3):
    vector.x = align_coord_to_voxel_object(vector.x)
    vector.y = align_coord_to_voxel_object(vector.y)
    vector.z = align_coord_to_voxel_object(vector.z)

    return vector

class CreateVoxelObjectResult:
    address         : int               = None

    value           : int
    voxel_object    : VoxelObject       = None

    def __init__(self, value: int, voxel_object: VoxelObject):
        self.value = value
        self.voxel_object = voxel_object
    
    def is_success(self) -> bool:
        return self.value == 0
    
    def get_meesage(self) -> str:
        value = self.value

        if value == 0:
            return "CREATE_VOXEL_OBJECT_SUCCESS"
        elif value == 1:
            return "CREATE_VOXEL_OBJECT_ALREADY_EXISTS"
        elif value == 2:
            return "CREATE_VOXEL_OBJECT_POSITION_ERROR"
        elif value == 3:
            return "CREATE_VOXEL_OBJECT_ALLOCATION_ERROR"

        return "CREATE_VOXEL_OBJECT_UNKNOWN"

IS_FUNCTION_LOAD = False

FUNCTION_CREATE_VOXEL_OBJECT = None
FUNCTION_GET_VOXEL_OBJECT_WITH_FLOAT_COORD = None
FUNCTION_UPDATE_VISIBILITY = None

def load_functions(client_context: ClientContext, voxel_object_manager_address: int):
    global IS_FUNCTION_LOAD
    
    if IS_FUNCTION_LOAD:
        return

    IS_FUNCTION_LOAD = True
    
    voxel_object_manager_function_table_address = read_memory(
        voxel_object_manager_address,
        ctypes.c_void_p
    )

    function_create_voxel_object_address = read_memory(
        voxel_object_manager_function_table_address + VOXEL_OBJECT_MANAGER_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT_MANAGER']['FUNCTION']['CREATE_VOXEL_OBJECT'], 
        ctypes.c_void_p
    )
    global FUNCTION_CREATE_VOXEL_OBJECT
    FUNCTION_CREATE_VOXEL_OBJECT = ctypes.CFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT, wintypes.UINT, wintypes.LPVOID)(function_create_voxel_object_address)

    function_get_voxel_object_with_float_coord_address = read_memory(
        voxel_object_manager_function_table_address + VOXEL_OBJECT_MANAGER_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT_MANAGER']['FUNCTION']['GET_VOXEL_OBJECT_WITH_FLOAT_COORD'], 
        ctypes.c_void_p
    )
    global FUNCTION_GET_VOXEL_OBJECT_WITH_FLOAT_COORD
    FUNCTION_GET_VOXEL_OBJECT_WITH_FLOAT_COORD = ctypes.CFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_get_voxel_object_with_float_coord_address)
    
    function_update_visibility_address = read_memory(
        voxel_object_manager_function_table_address + VOXEL_OBJECT_MANAGER_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT_MANAGER']['FUNCTION']['UPDATE_VISIBILITY'], 
        ctypes.c_void_p
    )
    global FUNCTION_UPDATE_VISIBILITY
    FUNCTION_UPDATE_VISIBILITY = ctypes.CFUNCTYPE(None, wintypes.LPVOID)(function_update_visibility_address)

class VoxelObjectManager:
    client_context          : ClientContext     = None
    address                 : int               = None
    
    def __init__(self, client_context: ClientContext, address: int):
        self.client_context = client_context
        self.address = address
        self.voxel_object_manager_address = self.address + VOXEL_OBJECT_MANAGER_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT_MANAGER']['OFFSET']
        
        load_functions(client_context, self.voxel_object_manager_address)
    
    def create_voxel_object(self, x: int, y: int, z: int, width_depth_height: int, color: int) -> CreateVoxelObjectResult:
        vector3 = Vector3()
        vector3.x = x
        vector3.y = y
        vector3.z = z

        return self.create_voxel_object(vector3, width_depth_height, color)
        
    def create_voxel_object_with_float_coord(self, vector: Vector3, width_depth_height: int, color: int) -> CreateVoxelObjectResult:
        align_vector3_to_voxel_object(vector)

        result = ctypes.c_int()
        address = FUNCTION_CREATE_VOXEL_OBJECT(self.voxel_object_manager_address, ctypes.addressof(vector), width_depth_height, color, ctypes.addressof(result))

        voxel_object = None

        if address:
            voxel_object = VoxelObject(self.client_context, address)
        
        return CreateVoxelObjectResult(result.value, voxel_object)
    
    def get_voxel_object(self, x: int, y: int, z: int) -> VoxelObject:
        vector3 = Vector3()
        vector3.x = x
        vector3.y = y
        vector3.z = z

        return self.get_voxel_object_with_float_coord(vector3)

    def get_voxel_object_with_float_coord(self, vector: Vector3) -> VoxelObject:
        address = FUNCTION_GET_VOXEL_OBJECT_WITH_FLOAT_COORD(self.voxel_object_manager_address, ctypes.addressof(vector))

        if address:
            return VoxelObject(self.client_context, address)
        
        return None

    def update_visibility(self):
        FUNCTION_UPDATE_VISIBILITY(self.voxel_object_manager_address)
    