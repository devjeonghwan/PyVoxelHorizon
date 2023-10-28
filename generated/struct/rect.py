import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enum import *

class Rect(ctypes.Structure):
    _fields_ = (
        ('left', wintypes.LONG),
        ('top', wintypes.LONG),
        ('right', wintypes.LONG),
        ('bottom', wintypes.LONG),
    )

    def __repr__(self):
        return f'Rect(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})'
