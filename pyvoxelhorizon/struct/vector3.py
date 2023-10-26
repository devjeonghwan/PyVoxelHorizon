import ctypes


class Vector3(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
    )

    def __repr__(self):
        return f'Vector3(x={self.x}, y={self.y}, z={self.z})'
