import ctypes
import ctypes.wintypes as wintypes

class IntAABB(ctypes.Structure):
    _fields_ = (
        ('min', IntVector3),
        ('max', IntVector3),
    )

    def __repr__(self):
        return f'IntAABB(min={self.min}, max={self.max})'
