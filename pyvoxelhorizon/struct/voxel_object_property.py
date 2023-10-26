import ctypes
import ctypes.wintypes as wintypes


class VoxelObjectProperty(ctypes.Structure):
    _fields_ = (
        ('width_depth_height', wintypes.UINT),
        ('voxel_size', ctypes.c_float),
    )

    def __repr__(self):
        return f'VoxelObjectProperty(width_depth_height={self.width_depth_height}, voxel_size={self.voxel_size})'
