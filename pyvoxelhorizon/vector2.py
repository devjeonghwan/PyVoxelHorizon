import ctypes
import ctypes.wintypes as wintypes

class Vector2(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
    )

    def __repr__(self):
        return f'Vector2(x={self.x}, y={self.y})'
