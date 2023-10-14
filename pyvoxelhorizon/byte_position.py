import ctypes
import ctypes.wintypes as wintypes

class BytePosition(ctypes.Structure):
    _fields_ = (
        ('x', wintypes.BYTE),
        ('y', wintypes.BYTE),
        ('z', wintypes.BYTE),
        ('reserved', wintypes.BYTE),
    )

    def __repr__(self):
        return f'BytePosition(x={self.x}, y={self.y}, z={self.z}, reserved={self.reserved})'
