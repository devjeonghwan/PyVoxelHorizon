from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

# Structs
from .vector3 import Vector3

# Objects
from .client_context import ClientContext
from .game_context import GameContext

from .battle_scene import BattleScene

from .voxel_object_manager import VoxelObjectManager, CreateVoxelObjectResult, align_vector3_to_voxel_object, align_coord_to_voxel_object

from .voxel_object import VoxelObject, VoxelObjectProperty, VoxelColor, find_similar_voxel_color, get_voxel_color

__all__ = [
    "get_client_context", 
    "get_game_context", 
    
    "Vector3",

    "ClientContext", 
    "GameContext", 
    
    "BattleScene", 
    
    "VoxelObjectManager",
    "CreateVoxelObjectResult",
    "align_vector3_to_voxel_object",
    "align_coord_to_voxel_object",

    "VoxelObject",
    "VoxelObjectProperty",
    "VoxelColor",
    "find_similar_voxel_color",
    "get_voxel_color",
]

def get_client_context(address) -> ClientContext:
    return ClientContext(address)

def get_game_context(client_context: ClientContext) -> GameContext:
    address = read_pointer_chain(client_context.address, [GLOBAL_OFFSET['STATIC']['GAME']])

    if address:
        return GameContext(client_context, address)
    
    return None