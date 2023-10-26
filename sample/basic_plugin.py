from abc import ABC

from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.type import *

PLUGIN_NAME = "BasicPlugin"


class BasicPlugin(Plugin, ABC):
    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def on_update(self):
        pass

    def on_command(self, command: str) -> bool:
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
