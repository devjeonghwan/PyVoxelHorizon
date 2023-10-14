import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enums import *

class Vertex(ctypes.Structure):
    _fields_ = (
        ('x', ctypes.c_float),
        ('y', ctypes.c_float),
        ('z', ctypes.c_float),
        ('nx', ctypes.c_float),
        ('ny', ctypes.c_float),
        ('nz', ctypes.c_float),
        ('u0', ctypes.c_float),
        ('v0', ctypes.c_float),
        ('u1', ctypes.c_float),
        ('v1', ctypes.c_float),
        ('dw_mesh_object_index', wintypes.DWORD),
        ('dw_face_group_index', wintypes.DWORD),
        ('dw_face_index', wintypes.DWORD),
        ('dw_mtl_index', wintypes.DWORD),
        ('p_data_ext', wintypes.LPVOID),
    )

    def __repr__(self):
        return f'Vertex(x={self.x}, y={self.y}, z={self.z}, nx={self.nx}, ny={self.ny}, nz={self.nz}, u0={self.u0}, v0={self.v0}, u1={self.u1}, v1={self.v1}, dw_mesh_object_index={self.dw_mesh_object_index}, dw_face_group_index={self.dw_face_group_index}, dw_face_index={self.dw_face_index}, dw_mtl_index={self.dw_mtl_index}, p_data_ext={self.p_data_ext})'
