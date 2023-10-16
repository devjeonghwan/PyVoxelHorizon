import sys
import os
import importlib

from types import ModuleType
from typing import List

from pyvoxelhorizon import GameHook
from pyvoxelhorizon.interface import GameController, NetworkLayer
from pyvoxelhorizon.plugin import Plugin


class PluginInfo:
    module: ModuleType = None
    name: str = None
    directory_path: str = None

    def __init__(self, module: ModuleType, name: str, directory_path: str):
        self.module = module
        self.name = name
        self.directory_path = directory_path

    def create_plugin(self) -> Plugin:
        return getattr(self.module, self.name)(self.directory_path)


class PluginLoader(GameHook):
    initialized: bool = False
    plugin_infos: List[PluginInfo] = []
    plugins: List[Plugin] = []

    game_controller: GameController = None
    network_layer: NetworkLayer = None
    plugin_directory_path: str = None

    def __init__(self, address):
        super().__init__(address)

    def on_start_scene(self, game_controller_address: int, network_layer_address: int, plugin_directory_path: str):
        if not self.game_controller:
            self.game_controller = GameController(game_controller_address)

        if not self.network_layer:
            self.network_layer = NetworkLayer(network_layer_address)

        if not self.plugin_directory_path:
            self.plugin_directory_path = plugin_directory_path

        if not self.initialized:
            py_voxel_horizon_directory_path = os.path.join(self.plugin_directory_path, "PyVoxelHorizon")
            plugins_directory_path = os.path.join(py_voxel_horizon_directory_path, "plugins")

            sys.path.append(py_voxel_horizon_directory_path)
            sys.path.append(plugins_directory_path)

            os.makedirs(plugins_directory_path, exist_ok=True)

            for file in os.listdir(plugins_directory_path):
                if file.casefold().endswith('.py'):
                    plugin_name = file[:-3]

                    module = importlib.import_module("plugins." + plugin_name)
                    plugin_name = getattr(module, "PLUGIN_NAME")

                    plugin_directory_path = os.path.join(plugins_directory_path, plugin_name)
                    os.makedirs(plugin_directory_path, exist_ok=True)

                    plugin_info = PluginInfo(module, plugin_name, plugin_directory_path)
                    self.plugin_infos.append(plugin_info)

            self.refresh_all_plugins()

            self.initialized = True

    def refresh_all_plugins(self):
        for plugin in self.plugins:
            plugin.on_destroy()

        self.plugins = []
        importlib.invalidate_caches()

        for plugin_info in self.plugin_infos:
            importlib.reload(plugin_info.module)

            plugin = plugin_info.create_plugin()
            plugin.on_create()

            self.plugins.append(plugin)

    def on_console_command(self, command: str) -> bool:
        if command.lower() == "reload_plugins":
            self.refresh_all_plugins()
            return True

        for plugin in self.plugins:
            if plugin.on_command(command):
                return True

        return False
