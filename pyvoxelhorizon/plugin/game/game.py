from pyvoxelhorizon.interface import *

from pyvoxelhorizon.plugin.util import *


class Game:
    controller: GameController
    network_layer: NetworkLayer

    def __init__(self, game_controller: GameController, network_layer: NetworkLayer):
        self.controller = game_controller
        self.network_layer = network_layer

    def print_text_to_system_dialog(self, message: str, color: Color = Color(255, 255, 255)):
        self.controller.write_text_to_system_dlg_w(color.get_argb(), message)

    def print_line_to_system_dialog(self, message: str, color: Color = Color(255, 255, 255)):
        self.controller.write_text_to_system_dlg_w(color.get_argb(), message + "\n")

    def print_to_console(self, message: str, color: Color = Color(255, 255, 255)):
        self.controller.write_text_to_console(message, len(message), color.get_argb())
