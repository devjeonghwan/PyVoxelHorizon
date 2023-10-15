from pyvoxelhorizon import GameHook
from pyvoxelhorizon.interface import GameController, NetworkLayer
from pyvoxelhorizon.struct import AABB, MidiNote, Vector3
from pyvoxelhorizon.enum import *
from pyvoxelhorizon.util import *

import ctypes
import ctypes.wintypes as wintypes
import tkinter.messagebox

def create_game_hook(address):
    return PyVoxelHorizonPluginLoader(address)

class PyVoxelHorizonPluginLoader(GameHook):
    game_controller     : GameController    = None
    network_layer       : NetworkLayer      = None
    plugin_path         : str               = None

    def __init__(self, address):
        super().__init__(address)

    def on_start_scene(self, game_controller_address: int, network_layer_address: int, plugin_path: str):
        if not self.game_controller:
            self.game_controller = GameController(game_controller_address)
            
        if not self.network_layer:
            self.network_layer = NetworkLayer(network_layer_address)
            
        if not self.plugin_path:
            self.plugin_path = plugin_path

        return
    
    def on_console_command(self, command: str) -> bool:
        return False