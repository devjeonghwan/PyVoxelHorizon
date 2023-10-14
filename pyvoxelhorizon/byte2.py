import ctypes
import ctypes.wintypes as wintypes

class Byte2(ctypes.Structure):
    _fields_ = (
        ('x', wintypes.BYTE),
        ('y', wintypes.BYTE),
    )

    def __repr__(self):
        return f'Byte2(x={self.x}, y={self.y})'
