from pyvoxelhorizon.game.offset import *
from pyvoxelhorizon.game.util import *

from .client_context import ClientContext
from .game_context import GameContext

from .battle_scene import BattleScene

from .key_code import *

from .vector3 import Vector3

from .voxel_object_manager import VoxelObjectManager, CreateVoxelObjectResult
from .voxel_object_manager import align_vector3_to_voxel_object, align_coord_to_voxel_object

from .voxel_color import VoxelColor, find_similar_voxel_color, get_voxel_color
from .voxel_object import VoxelObject, VoxelObjectProperty

__all__ = [
    "get_client_context", 
    "get_game_context", 
    
    "ClientContext", 
    "GameContext", 

    "BattleScene", 
    
    "KeyCode",
    "get_key_code",

    "Vector3",

    "VoxelObjectManager",
    "CreateVoxelObjectResult",
    "align_vector3_to_voxel_object",
    "align_coord_to_voxel_object",

    "VoxelColor",
    "find_similar_voxel_color",
    "get_voxel_color",
    
    "VoxelObject",
    "VoxelObjectProperty",
] + key_code_names

def get_client_context(address) -> ClientContext:
    return ClientContext(address)

def get_game_context(client_context: ClientContext) -> GameContext:
    address = read_pointer_chain(client_context.address, [GLOBAL_OFFSET['STATIC']['GAME']])

    if address:
        return GameContext(client_context, address)
    
    return None