from voxel_horizon_plugin import VoxelHorizonPlugin
from pyvoxelhorizon.game.object import *

import pyvoxelhorizon

import sys
import os
import importlib
import ctypes

class PyVoxelHorizon:
    client_context      : ClientContext             = None
    game_context        : GameContext               = None
    working_directory   : str                       = None
    plugins             : list[VoxelHorizonPlugin]  = []

    def __init__(self, working_directory: str):
        self.working_directory = working_directory

    def on_initialize(self, module_address: int, game_object_address: int):
        self.client_context = get_client_context(module_address)
        self.game_context = get_game_context(self.client_context)

        if self.game_context is None:
            print("Cannot find `CGame` instance in memory.")
            exit()

        self.game_object_address = game_object_address

        # Load Plugins
        sys.path.append(self.working_directory)

        for file in os.listdir(os.path.join(self.working_directory, "plugins")):
            if file.casefold().endswith('.py'):
                plugin_name = file[:-3]
                
                module = importlib.import_module("plugins." + plugin_name, package="plugins")
                
                plugin_name = getattr(module, "PLUGIN_NAME")

                self.plugins.append(getattr(module, plugin_name)(self.working_directory))
       
        for plugin in self.plugins:
            plugin.on_initialize(self.game_context)

    def on_loop(self):
        for plugin in self.plugins:
            plugin.update(self.game_context)
        
    def on_stop(self):
        for plugin in self.plugins:
            plugin.on_stop()

# Injection
if __name__ == "__main__":
    pyvoxelhorizon.patch_with_python_script(os.path.realpath(__file__))
