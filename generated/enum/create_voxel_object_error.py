import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *

CREATE_VOXEL_OBJECT_ERROR_OK = 0
CREATE_VOXEL_OBJECT_ERROR_ALREADY_EXIST = 1
CREATE_VOXEL_OBJECT_ERROR_INVALID_POS = 2
CREATE_VOXEL_OBJECT_ERROR_FAIL_ALLOC_INDEX = 3


def get_create_voxel_object_error_string(value: int):
    if value == 0:
        return 'CREATE_VOXEL_OBJECT_ERROR_OK'
    if value == 1:
        return 'CREATE_VOXEL_OBJECT_ERROR_ALREADY_EXIST'
    if value == 2:
        return 'CREATE_VOXEL_OBJECT_ERROR_INVALID_POS'
    if value == 3:
        return 'CREATE_VOXEL_OBJECT_ERROR_FAIL_ALLOC_INDEX'
    
    return 'CREATE_VOXEL_OBJECT_ERROR_UNKNOWN'
