import ctypes
import ctypes.wintypes as wintypes

class IndexPosition(ctypes.Structure):
    _fields_ = (
        ('dw_x', wintypes.DWORD),
        ('dw_y', wintypes.DWORD),
    )

    def __repr__(self):
        return f'IndexPosition(dw_x={self.dw_x}, dw_y={self.dw_y})'
