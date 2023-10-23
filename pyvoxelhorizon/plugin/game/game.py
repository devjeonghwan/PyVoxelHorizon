from pyvoxelhorizon.enum import *
from pyvoxelhorizon.interface import *
from pyvoxelhorizon.struct import *

from pyvoxelhorizon.plugin.util import *


class Game:
    game_controller: GameController = None
    network_layer: NetworkLayer = None

    def __init__(self, game_controller: GameController, network_layer: NetworkLayer):
        self.game_controller = game_controller
        self.network_layer = network_layer

    def print_text_to_system_dialog(self, message: str, color: Color = Color(255, 255, 255)):
        self.game_controller.write_text_to_system_dlg_w(color.get_argb(), message)

    def print_line_to_system_dialog(self, message: str, color: Color = Color(255, 255, 255)):
        self.game_controller.write_text_to_system_dlg_w(color.get_argb(), message + "\n")
