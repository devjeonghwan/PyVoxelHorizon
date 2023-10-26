import ctypes
import ctypes.wintypes as wintypes


class VoxelDescriptionLite(ctypes.Structure):
    _fields_ = (
        ('p_voxel_obj', wintypes.LPVOID),
        ('x', ctypes.c_int),
        ('y', ctypes.c_int),
        ('z', ctypes.c_int),
        ('color_index', wintypes.BYTE),
    )

    def __repr__(self):
        return f'VoxelDescriptionLite(p_voxel_obj={self.p_voxel_obj}, x={self.x}, y={self.y}, z={self.z}, color_index={self.color_index})'
