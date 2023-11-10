from abc import ABC
from ctypes import wintypes

from pyvoxelhorizon.enum import *
from pyvoxelhorizon.interface import *
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.plugin.game.voxel import VoxelColor, VOXEL_COLOR_PALETTE
from pyvoxelhorizon.plugin.game.voxel import VoxelEditor
from pyvoxelhorizon.struct import *

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

        return_value = self.game_controller.get_single_voxel_color_with_float_coord(self.output_color_index, self.input_vector3)

        if return_value == SINGLE_VOXEL_EDIT_RESULT_NO_VOXEL:
            return False

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            raise Exception("Failed to get voxel color. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

        return True

    def set_voxel(self, x: int, y: int, z: int, value: bool):
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        if value:
            return_value = self.game_controller.set_single_voxel_with_float_coord(self.input_vector3, 0)

            if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
                raise Exception("Failed to set voxel. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))
        else:
            return_value = self.game_controller.remove_single_voxel_with_float_coord(self.input_vector3)

            if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
                raise Exception("Failed to remove voxel. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

    def set_voxel_with_color(self, x: int, y: int, z: int, value: bool, color: VoxelColor):
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        if value:
            return_value = self.game_controller.set_single_voxel_with_float_coord(self.input_vector3, color.index)

            if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
                raise Exception("Failed to set voxel. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))
        else:
            return_value = self.game_controller.remove_single_voxel_with_float_coord(self.input_vector3)

            if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
                raise Exception("Failed to remove voxel. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

    def get_voxel_color(self, x: int, y: int, z: int) -> VoxelColor | None:
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        return_value = self.game_controller.get_single_voxel_color_with_float_coord(self.output_color_index, self.input_vector3)

        if return_value == SINGLE_VOXEL_EDIT_RESULT_NO_VOXEL:
            return None

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            raise Exception("Failed to get voxel color. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

        return VOXEL_COLOR_PALETTE[self.output_color_index.value]

    def set_voxel_color(self, x: int, y: int, z: int, color: VoxelColor) -> bool:
        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        return_value = self.game_controller.get_single_voxel_color_with_float_coord(self.output_color_index, self.input_vector3)

        if return_value == SINGLE_VOXEL_EDIT_RESULT_NO_VOXEL:
            return False

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            raise Exception("Failed to get voxel color. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

        return_value = self.game_controller.set_single_voxel_with_float_coord(self.input_vector3, color.index)

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            raise Exception("Failed to set voxel color. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

        return True

    def finish(self):
        pass
