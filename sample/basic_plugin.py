import tkinter.messagebox

from abc import ABC

from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.util import *
from pyvoxelhorizon.plugin.type import *
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.plugin.game.voxel import *

PLUGIN_NAME = "BasicPlugin"


class BasicPlugin(Plugin, ABC):
    index: int = 0

    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def on_update(self):
        pass

    def on_command(self, command: str) -> bool:
        if command == "test":
            self.game.print_text_to_system_dialog(Color(255, 255, 255), "Test!")

            return True

        if command == "draw":
            voxel_editor = VoxelEditor(self.game)

            x = 1000
            y = -2350
            z = 1100

            voxel_editor.add_voxel(
                x + (self.index * 50),
                y + (self.index * 50),
                z,
                get_voxel_color(0)
            )

            voxel_editor.add_voxel(
                x,
                y,
                z + (self.index * 50),
                get_voxel_color(0)
            )

            self.index += 1

            voxel_editor.finish()

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
