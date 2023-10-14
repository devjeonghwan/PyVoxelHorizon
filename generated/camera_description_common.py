import ctypes
import ctypes.wintypes as wintypes

class CameraDescriptionCommon(ctypes.Structure):
    _fields_ = (
        ('v3_from', Vector3),
        ('v3_up', Vector3),
        ('v3_eye_dir', Vector3),
        ('f_near', ctypes.c_float),
        ('f_far', ctypes.c_float),
    )

    def __repr__(self):
        return f'CameraDescriptionCommon(v3_from={self.v3_from}, v3_up={self.v3_up}, v3_eye_dir={self.v3_eye_dir}, f_near={self.f_near}, f_far={self.f_far})'
