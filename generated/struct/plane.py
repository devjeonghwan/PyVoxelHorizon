import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enums import *
from pyvoxelhorizon.struct.vector3 import Vector3

class Plane(ctypes.Structure):
    _fields_ = (
        ('v3_up', Vector3),
        ('d', ctypes.c_float),
    )

    def __repr__(self):
        return f'Plane(v3_up={self.v3_up}, d={self.d})'
