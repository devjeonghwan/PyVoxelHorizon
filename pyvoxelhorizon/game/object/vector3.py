import ctypes
import ctypes.wintypes as wintypes
import struct

class Vector3(ctypes.Structure):
    x: float
    y: float
    z: float

    _fields_ = (
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float)
    )

    def __repr__(self):
        return f'Vector3(x={self.x}, y={self.y}, z={self.z})'