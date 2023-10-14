import ctypes
import ctypes.wintypes as wintypes

class IntVector2(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
    )

    def __repr__(self):
        return f'IntVector2(x={self.x}, y={self.y})'
