import pyvoxelhorizon
from pyvoxelhorizon.game.object import *

import sys
import os
import importlib
import ctypes

class PyVoxelHorizon:
    def __init__(self, working_directory):
        # Setup Fields
        self.client_context = None
        self.working_directory = working_directory
        self.plugins = []

    def on_initialize(self, module_address, game_object_address):
        self.client_context = ClientContext(module_address)

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
            plugin.on_initialize(self.client_context)

    def on_loop(self):
        game_object = self.client_context.get_game()

        for plugin in self.plugins:
            plugin.on_loop(game_object)
        
    def on_stop(self):
        for plugin in self.plugins:
            plugin.on_stop()

# Injection
if __name__ == "__main__":
    pyvoxelhorizon.patch_with_python_script(os.path.realpath(__file__))
