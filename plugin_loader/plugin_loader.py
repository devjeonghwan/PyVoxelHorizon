from pyvoxelhorizon import GameHook
from pyvoxelhorizon.interface import GameController
from pyvoxelhorizon.interface import NetworkLayer
from pyvoxelhorizon.struct import AABB

import ctypes
import ctypes.wintypes as wintypes
import tkinter.messagebox

def create_game_hook(address):
    return PyVoxelHorizonPluginLoader(address)

class PyVoxelHorizonPluginLoader(GameHook):
    game_controller     : GameController    = None
    network_layer       : NetworkLayer      = None

    def __init__(self, address):
        return
    
    def on_start_scene(self, game_controller_address: int, network_layer_address: int, plugin_path: str):
        if not self.game_controller:
            self.game_controller = GameController(game_controller_address)
            
        if not self.network_layer:
            self.network_layer = NetworkLayer(network_layer_address)

        num_width = wintypes.DWORD()
        num_depth = wintypes.DWORD()
        num_height = wintypes.DWORD()
        world_aabb = AABB()

        self.game_controller.get_world_info(num_width, num_depth, num_height, world_aabb)

        self.game_controller.write_text_to_system_dlg_w(0xFFFFFFFF, str((num_width.value, num_depth.value, num_height.value)) + "\n")
        self.game_controller.write_text_to_system_dlg_w(0xFFFFFFFF, str(world_aabb) + "\n")

        return
    

    