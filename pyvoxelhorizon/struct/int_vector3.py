import ctypes


class IntVector3(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('z', ctypes.c_int),
    )

    def __repr__(self):
        return f'IntVector3(x={self.x}, y={self.y}, z={self.z})'
