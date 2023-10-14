import ctypes
import ctypes.wintypes as wintypes

class Plane(ctypes.Structure):
    _fields_ = (
        ('v3_up', Vector3),
        ('d', ctypes.c_float),
    )

    def __repr__(self):
        return f'Plane(v3_up={self.v3_up}, d={self.d})'
