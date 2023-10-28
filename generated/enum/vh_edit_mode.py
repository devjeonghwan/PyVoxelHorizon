import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *

VH_EDIT_MODE_SELECT = 0
VH_EDIT_MODE_CREATE_NEW_OBJECT = 1
VH_EDIT_MODE_SET_VOXEL_COLOR = 2
VH_EDIT_MODE_ADD_VOXEL = 3
VH_EDIT_MODE_REMOVE_VOXEL = 4
VH_EDIT_MODE_COUNT = 5


def get_vh_edit_mode_string(value: int):
    if value == 0:
        return 'VH_EDIT_MODE_SELECT'
    if value == 1:
        return 'VH_EDIT_MODE_CREATE_NEW_OBJECT'
    if value == 2:
        return 'VH_EDIT_MODE_SET_VOXEL_COLOR'
    if value == 3:
        return 'VH_EDIT_MODE_ADD_VOXEL'
    if value == 4:
        return 'VH_EDIT_MODE_REMOVE_VOXEL'
    if value == 5:
        return 'VH_EDIT_MODE_COUNT'
    
    return 'VH_EDIT_MODE_UNKNOWN'
