import ctypes
import ctypes.wintypes as wintypes

class AABB(ctypes.Structure):
    _fields_ = (
        ('min', Vector3),
        ('max', Vector3),
    )

    def __repr__(self):
        return f'AABB(min={self.min}, max={self.max})'
