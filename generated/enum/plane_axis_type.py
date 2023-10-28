import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *

PLANE_AXIS_TYPE_XZ = 0
PLANE_AXIS_TYPE_XY = 1
PLANE_AXIS_TYPE_YZ = 2
PLANE_AXIS_TYPE_COUNT = 3


def get_plane_axis_type_string(value: int):
    if value == 0:
        return 'PLANE_AXIS_TYPE_XZ'
    if value == 1:
        return 'PLANE_AXIS_TYPE_XY'
    if value == 2:
        return 'PLANE_AXIS_TYPE_YZ'
    if value == 3:
        return 'PLANE_AXIS_TYPE_COUNT'
    
    return 'PLANE_AXIS_TYPE_UNKNOWN'
