from abc import ABC
from ctypes import wintypes

from pyvoxelhorizon.interface import *
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.struct import *
from pyvoxelhorizon.plugin.game.voxel import VoxelEditor
from pyvoxelhorizon.plugin.game.voxel import VoxelColor, VOXEL_COLOR_PALETTE

VOXEL_OBJECT_SIZE = 400
VOXEL_OBJECT_8_SIZE = int(VOXEL_OBJECT_SIZE / 8)
VOXEL_OBJECT_HALF_SIZE = int(VOXEL_OBJECT_SIZE / 2)

BIT_SELECTORS = [
    0b1 << 0,
    0b1 << 1,
    0b1 << 2,
    0b1 << 3,
    0b1 << 4,
    0b1 << 5,
    0b1 << 6,
    0b1 << 7,
]

BIT_REVERSE_SELECTORS = [
    ~(0b1 << 0),
    ~(0b1 << 1),
    ~(0b1 << 2),
    ~(0b1 << 3),
    ~(0b1 << 4),
    ~(0b1 << 5),
    ~(0b1 << 6),
    ~(0b1 << 7),
]


class VoxelEditorOnline(VoxelEditor, ABC):
    game_controller: GameController

    input_vector3: Vector3
    output_color_index: wintypes.BYTE

    def __init__(self, game: Game):
        self.game_controller = game.controller

        self.input_vector3 = Vector3()
        self.output_color_index = wintypes.BYTE()

    def get_voxel(self, x: int, y: int, z: int) -> bool:
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        return self.game_controller.get_voxel_color_with_float_coord(self.output_color_index, self.input_vector3, 8)

    def set_voxel(self, x: int, y: int, z: int, value: bool):
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        if value:
            color_index = 0

            if self.game_controller.get_voxel_color_with_float_coord(self.output_color_index, self.input_vector3, 8):
                color_index = self.output_color_index.value

            self.game_controller.set_voxel_with_float_coord(self.input_vector3, 8, color_index, False)
        else:
            self.game_controller.remove_voxel_with_float_coord(self.input_vector3, 8, 0, False)

    def set_voxel_with_color(self, x: int, y: int, z: int, value: bool, color: VoxelColor):
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        if value:
            self.game_controller.set_voxel_with_float_coord(self.input_vector3, 8, color.index, False)
        else:
            self.game_controller.remove_voxel_with_float_coord(self.input_vector3, 8, color.index, False)

    def get_voxel_color(self, x: int, y: int, z: int) -> VoxelColor | None:
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        if self.game_controller.get_voxel_color_with_float_coord(self.output_color_index, self.input_vector3, 8):
            return VOXEL_COLOR_PALETTE[self.output_color_index.value]

        return None

    def set_voxel_color(self, x: int, y: int, z: int, color: VoxelColor) -> bool:
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        exists = self.game_controller.get_voxel_color_with_float_coord(self.output_color_index, self.input_vector3, 8)

        if exists:
            return self.game_controller.set_voxel_with_float_coord(self.input_vector3, 8, color.index, False)

        return False

    def finish(self):
        pass
