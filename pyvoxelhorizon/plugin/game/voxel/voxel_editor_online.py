from abc import ABC
from ctypes import wintypes
from typing import Callable

from pyvoxelhorizon.enum import *
from pyvoxelhorizon.interface import *
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.plugin.game.voxel import VoxelColor, VOXEL_COLOR_PALETTE
from pyvoxelhorizon.plugin.game.voxel import VoxelEditor
from pyvoxelhorizon.struct import *

VOXEL_EDITING_QUEUE = []
VOXEL_EDITING_VECTOR3 = Vector3()


def get_vector(x: float, y: float, z: float):
    VOXEL_EDITING_VECTOR3.x = x
    VOXEL_EDITING_VECTOR3.y = y
    VOXEL_EDITING_VECTOR3.z = z

    return VOXEL_EDITING_VECTOR3


def append_editing_queue(editing_func: Callable):
    VOXEL_EDITING_QUEUE.append(editing_func)


def process_editing_queue():
    while True:
        if len(VOXEL_EDITING_QUEUE) <= 0:
            return SINGLE_VOXEL_EDIT_RESULT_OK

        editing_func = VOXEL_EDITING_QUEUE[0]

        return_value = editing_func()

        if return_value == SINGLE_VOXEL_EDIT_RESULT_BUFFER_NOT_ENOUGH:
            return SINGLE_VOXEL_EDIT_RESULT_OK
        else:
            VOXEL_EDITING_QUEUE.pop(0)

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            return return_value


def wait_for_editing_queue():
    while True:
        if len(VOXEL_EDITING_QUEUE) <= 0:
            return

        process_editing_queue()


def cancel_all_editing_queue(game: Game):
    VOXEL_EDITING_QUEUE.clear()
    game.controller.cancel_all_pending_voxel_edit_event()


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
        if value:
            append_editing_queue(lambda: self.game_controller.set_single_voxel_with_float_coord(get_vector(x, y, z), 0))
        else:
            append_editing_queue(lambda: self.game_controller.remove_single_voxel_with_float_coord(get_vector(x, y, z)))

        return_value = process_editing_queue()

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            raise Exception("Failed to editing voxel. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

    def set_voxel_with_color(self, x: int, y: int, z: int, value: bool, color: VoxelColor = VOXEL_COLOR_PALETTE[0]):
        if value:
            append_editing_queue(lambda: self.game_controller.set_single_voxel_with_float_coord(get_vector(x, y, z), color.index))
        else:
            append_editing_queue(lambda: self.game_controller.remove_single_voxel_with_float_coord(get_vector(x, y, z)))

        return_value = process_editing_queue()

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            raise Exception("Failed to editing voxel. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

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

        append_editing_queue(lambda: self.game_controller.set_single_voxel_with_float_coord(get_vector(x, y, z), color.index))

        return_value = process_editing_queue()

        if return_value != SINGLE_VOXEL_EDIT_RESULT_OK:
            raise Exception("Failed to editing voxel. returned `{0}`.".format(get_single_voxel_edit_result_string(return_value)))

        return True

    def finish(self):
        pass
