from pyvoxelhorizon import GameHook
from pyvoxelhorizon.interface import GameController
from pyvoxelhorizon.interface import NetworkLayer
from pyvoxelhorizon.struct import AABB
from pyvoxelhorizon.struct import Vector3
from pyvoxelhorizon.enum import *

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
    
    def on_console_command(self, command: str) -> bool:
        if command == "create_test_voxel":
            vector = Vector3()
            vector.x = 1000.0
            vector.y = -1000.0
            vector.z = 200.0

            out_error_code = wintypes.INT()

            new_voxel_object = self.game_controller.create_voxel_object(vector, 1, 26, out_error_code)

            self.game_controller.write_text_to_system_dlg_w(0xFFFFFFFF, "Error Code: {0}\n".format(out_error_code.value))

            if new_voxel_object:
                out_new_width_depth_height = wintypes.UINT()

                ret_add_voxel = new_voxel_object.add_voxel_with_auto_resize(out_new_width_depth_height, 0, 0, 0, 26, 8)

                self.game_controller.write_text_to_system_dlg_w(0xFFFFFFFF, "Return: {0}\n".format(ret_add_voxel))

                new_voxel_object.update_geometry(False)
                new_voxel_object.update_lighting()
            
            return True

        return False