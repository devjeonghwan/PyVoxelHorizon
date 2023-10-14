import ctypes
import ctypes.wintypes as wintypes

class WordPosition(ctypes.Structure):
    _fields_ = (
        ('w_x', wintypes.WORD),
        ('w_z', wintypes.WORD),
    )

    def __repr__(self):
        return f'WordPosition(w_x={self.w_x}, w_z={self.w_z})'
