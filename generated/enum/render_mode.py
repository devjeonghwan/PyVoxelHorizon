import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *

RENDER_MODE_SOLID = 0x00000000
RENDER_MODE_POINT = 0x00000001
RENDER_MODE_WIREFRAME = 0x00000002


def get_render_mode_string(value: int):
    if value == 0x00000000:
        return 'RENDER_MODE_SOLID'
    if value == 0x00000001:
        return 'RENDER_MODE_POINT'
    if value == 0x00000002:
        return 'RENDER_MODE_WIREFRAME'
    
    return 'RENDER_MODE_UNKNOWN'
