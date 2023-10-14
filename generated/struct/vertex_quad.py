import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enums import *
from pyvoxelhorizon.struct.vertex import Vertex

class VertexQuad(ctypes.Structure):
    _fields_ = (
        ('piv_list', Vertex * 4),
    )

    def __repr__(self):
        return f'VertexQuad(piv_list={self.piv_list})'
