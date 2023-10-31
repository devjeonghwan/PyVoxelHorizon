import math
import os
import time
from abc import ABC
from typing import List

import numpy
import umidiparser

from pyvoxelhorizon.plugin import Plugin
from pyvoxelhorizon.plugin.game.voxel import *
from pyvoxelhorizon.plugin.type import *

PLUGIN_NAME = "VoxelEditorExamplePlugin"


class VoxelEditorExamplePlugin(Plugin, ABC):
    index: int = 0

    def on_create(self):
        pass

    def on_destroy(self):
        pass

    def on_update(self):
        pass

    def on_command(self, command: str) -> bool:
        if command == 'edit':
            offset_x = 400
            offset_y = -2400
            offset_z = -1600

            voxel_editor = VoxelEditor(self.game)

            voxel_editor.set_voxel_with_color(
                offset_x + (self.index * 50),
                offset_y + (self.index * 50),
                offset_z + (self.index * 50),
                True,
                get_voxel_color(27)
            )

            voxel_editor.set_voxel_with_color(
                offset_x + (self.index * -50),
                offset_y + (self.index * 50),
                offset_z + (self.index * -50),
                True,
                get_voxel_color(27)
            )

            voxel_editor.finish()

            self.index += 1

            return True

        return False

    def on_mouse_click(self, x: int, y: int, button_type: MouseButtonType, pressed: bool) -> bool:
        return False

    def on_mouse_move(self, x: int, y: int) -> bool:
        return False

    def on_mouse_wheel(self, x: int, y: int, wheel: int) -> bool:
        return False

    def on_key(self, key_type: KeyType, pressed: bool) -> bool:
        return False

    def on_pad(self, button_type: PadButtonType, pressed: bool) -> bool:
        return False
