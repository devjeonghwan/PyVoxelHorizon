import ctypes
import ctypes.wintypes as wintypes

class DwordRectangle(ctypes.Structure):
    _fields_ = (
        ('left', wintypes.DWORD),
        ('top', wintypes.DWORD),
        ('right', wintypes.DWORD),
        ('bottom', wintypes.DWORD),
    )

    def __repr__(self):
        return f'DwordRectangle(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})'
