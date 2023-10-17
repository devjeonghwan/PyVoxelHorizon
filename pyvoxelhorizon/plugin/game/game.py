from pyvoxelhorizon.interface import *
from pyvoxelhorizon.struct import *

from pyvoxelhorizon.plugin.util import *


class Game:
    game_controller: GameController = None

    def __init__(self, game_controller: GameController):
        self.game_controller = game_controller

    def print_text_to_system_dialog(self, color: Color, message: str):
        self.game_controller.write_text_to_system_dlg_w(color.get_argb(), message)