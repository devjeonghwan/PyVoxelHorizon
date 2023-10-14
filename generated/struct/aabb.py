import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enums import *
from pyvoxelhorizon.struct.vector3 import Vector3

class AABB(ctypes.Structure):
    _fields_ = (
        ('min', Vector3),
        ('max', Vector3),
    )

    def __repr__(self):
        return f'AABB(min={self.min}, max={self.max})'
