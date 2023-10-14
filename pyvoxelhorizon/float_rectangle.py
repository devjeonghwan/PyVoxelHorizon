import ctypes
import ctypes.wintypes as wintypes

class FloatRectangle(ctypes.Structure):
    _fields_ = (
        ('f_left', ctypes.c_float),
        ('f_top', ctypes.c_float),
        ('f_right', ctypes.c_float),
        ('f_bottom', ctypes.c_float),
    )

    def __repr__(self):
        return f'FloatRectangle(f_left={self.f_left}, f_top={self.f_top}, f_right={self.f_right}, f_bottom={self.f_bottom})'
