import ctypes

from pyvoxelhorizon.struct.vector3 import Vector3


class BoundingSphere(ctypes.Structure):
    _fields_ = (
        ('v3_point', Vector3),
        ('f_rs', ctypes.c_float),
    )

    def __repr__(self):
        return f'BoundingSphere(v3_point={self.v3_point}, f_rs={self.f_rs})'
