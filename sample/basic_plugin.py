import tkinter.messagebox

from abc import ABC

from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.plugin.util import *
from pyvoxelhorizon.plugin.type import *

PLUGIN_NAME = "BasicPlugin"


class BasicPlugin(Plugin, ABC):
    def on_create(self):
        self.game.print_text_to_system_dialog(Color(255, 255, 255), "Test!")

    def on_destroy(self):
        pass

    def on_update(self):
        pass

    def on_command(self, command: str) -> bool:
        if command == "test":
            self.game.print_text_to_system_dialog(Color(255, 255, 255), "Test!")

            return True

        return False

    def on_mouse_click(self, x: int, y: int, button_type: MouseButtonType, pressed: bool) -> bool:
        return False

    def on_mouse_move(self, x: int, y: int) -> bool:
        return False

    def on_mouse_wheel(self, wheel: int) -> bool:
        return False

    def on_key(self, key_type: KeyType, pressed: bool) -> bool:
        return False

    def on_pad(self, button_type: PadButtonType, pressed: bool) -> bool:
        return False
