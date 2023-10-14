import ctypes
import ctypes.wintypes as wintypes

from .vector3 import Vector3

class Triangle(ctypes.Structure):
    _fields_ = (
        ('v3_point', Vector3 * 3),
    )

    def __repr__(self):
        return f'Triangle(v3_point={self.v3_point})'
