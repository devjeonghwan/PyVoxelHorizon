import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *

SINGLE_VOXEL_EDIT_RESULT_OK = 0
SINGLE_VOXEL_EDIT_RESULT_INVALID_POSITION = 1
SINGLE_VOXEL_EDIT_RESULT_BUFFER_NOT_ENOUGH = 2
SINGLE_VOXEL_EDIT_RESULT_NO_VOXEL = 3
SINGLE_VOXEL_EDIT_RESULT_UNKNWON_ERROR = 4


def get_single_voxel_edit_result_string(value: int):
    if value == 0:
        return 'SINGLE_VOXEL_EDIT_RESULT_OK'
    if value == 1:
        return 'SINGLE_VOXEL_EDIT_RESULT_INVALID_POSITION'
    if value == 2:
        return 'SINGLE_VOXEL_EDIT_RESULT_BUFFER_NOT_ENOUGH'
    if value == 3:
        return 'SINGLE_VOXEL_EDIT_RESULT_NO_VOXEL'
    if value == 4:
        return 'SINGLE_VOXEL_EDIT_RESULT_UNKNWON_ERROR'
    
    return 'SINGLE_VOXEL_EDIT_RESULT_UNKNOWN'
