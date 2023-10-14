from .game_hook import GameHook
from .game_controller import GameController
from .network_layer import NetworkLayer
from .voxel_object_lite import VoxelObjectLite

VH_EDIT_MODE_SELECT	 = 0
VH_EDIT_MODE_CREATE_NEW_OBJECT	 = 1
VH_EDIT_MODE_SET_VOXEL_COLOR	 = 2
VH_EDIT_MODE_ADD_VOXEL	 = 3
VH_EDIT_MODE_REMOVE_VOXEL	 = 4
VH_EDIT_MODE_COUNT	 = 5

__all__ = ['GameHook', 'GameController', 'NetworkLayer', 'VoxelObjectLite']