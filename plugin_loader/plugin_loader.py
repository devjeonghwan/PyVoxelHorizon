from pyvoxelhorizon import GameHook, GameController
import tkinter.messagebox

def create_game_hook(address):
    return PyVoxelHorizonPluginLoader(address)

class PyVoxelHorizonPluginLoader(GameHook):
    def __init__(self, address):
        return
    
    def on_start_scene(self, game_controller_address: int, network_layer_address: int, plugin_path: str):
        game_controller = GameController(game_controller_address)

        game_controller.write_text_to_system_dlg_w(0xFFFFFFFF, "Hello, Python!\n")

        number_of_voxel_object = game_controller.get_voxel_object_num()
        game_controller.write_text_to_system_dlg_w(0xFFF00FFF, "Number of Voxel Object: " + str(number_of_voxel_object))

        return