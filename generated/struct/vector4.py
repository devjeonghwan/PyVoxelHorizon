import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enum import *

class Vector4(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('w', ctypes.c_float),
    )

    def __repr__(self):
        return f'Vector4(x={self.x}, y={self.y}, z={self.z}, w={self.w})'
