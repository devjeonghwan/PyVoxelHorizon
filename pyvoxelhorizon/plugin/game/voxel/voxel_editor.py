import ctypes
from ctypes import wintypes

from pyvoxelhorizon.util.address_object import *
from pyvoxelhorizon.enum import *
from pyvoxelhorizon.interface import *
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.struct import *
from .voxel_color import VoxelColor, get_voxel_color, VOXEL_COLOR_PALETTE

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


# Always handle voxel object with '8' width depth height
class VoxelObject:
    voxel_object_lite: VoxelObjectLite = None

    dirty: bool = False
    bit_table: list[int] = None
    color_table: list[int] = None

    def __init__(self, voxel_object_lite: VoxelObjectLite):
        self.voxel_object_lite = voxel_object_lite

        out_bit_table = (ctypes.c_uint8 * 64)()
        out_width_depth_height = wintypes.UINT()

        if not self.voxel_object_lite.get_bit_table(cast_address(get_address(out_bit_table), ctypes.c_uint), 64, out_width_depth_height):
            raise Exception("Unreachable Exception")

        if out_width_depth_height.value != 8:
            if not self.voxel_object_lite.resize_width_depth_height(8, False):
                raise Exception("Failed to resize width depth height of voxel object.")

        if not self.voxel_object_lite.get_bit_table(cast_address(get_address(out_bit_table), ctypes.c_uint), 64, out_width_depth_height):
            raise Exception("Unreachable Exception")

        if out_width_depth_height.value != 8:
            raise Exception("Unreachable Exception")

        out_color_table = (ctypes.c_uint8 * 512)()

        if not self.voxel_object_lite.get_color_table(cast_address(get_address(out_color_table), wintypes.BYTE), 512, 8):
            raise Exception("Unreachable Exception")

        self.bit_table = list(out_bit_table)
        self.color_table = list(out_color_table)

    def apply_tables(self):
        if not self.dirty:
            return

        self.dirty = False

        bit_table = (ctypes.c_uint8 * len(self.bit_table))(*self.bit_table)

        self.voxel_object_lite.set_bit_table(cast_address(get_address(bit_table), ctypes.c_uint), 8, False)
        # if not self.voxel_object_lite.set_bit_table(cast_address(get_address(bit_table), ctypes.c_uint), 8, False):
        #     raise Exception("Failed to set bit table to voxel object.")

        color_table = (ctypes.c_uint8 * len(self.color_table))(*self.color_table)

        self.voxel_object_lite.set_color_table(cast_address(get_address(color_table), wintypes.BYTE), 8)
        # if not self.voxel_object_lite.set_color_table(cast_address(get_address(color_table), wintypes.BYTE), 8):
        #     raise Exception("Failed to set color table to voxel object.")

        self.voxel_object_lite.update_geometry(False)
        self.voxel_object_lite.update_lighting()

    def clear(self):
        for index in range(len(self.bit_table)):
            self.bit_table[index] = 0

    def get_voxel(self, x: int, y: int, z: int) -> bool:
        index = x + (z * 8) + (y * 64)

        byte_index = int(index / 8)
        bit_index = index % 8

        return self.bit_table[byte_index] & BIT_SELECTORS[bit_index] != 0

    def set_voxel(self, x: int, y: int, z: int, value: bool):
        self.dirty = True

        index = x + (z * 8) + (y * 64)

        byte_index = int(index / 8)
        bit_index = index % 8

        if value:
            self.bit_table[byte_index] |= BIT_SELECTORS[bit_index]
        else:
            self.bit_table[byte_index] &= BIT_REVERSE_SELECTORS[bit_index]

    def get_voxel_color(self, x: int, y: int, z: int) -> VoxelColor:
        index = x + (z * 8) + (y * 64)

        return VOXEL_COLOR_PALETTE[self.color_table[index]]

    def get_voxel_color_if_exists(self, x: int, y: int, z: int) -> VoxelColor | None:
        index = x + (z * 8) + (y * 64)

        byte_index = int(index / 8)
        bit_index = index % 8

        if self.bit_table[byte_index] & BIT_SELECTORS[bit_index] != 0:
            return VOXEL_COLOR_PALETTE[self.color_table[index]]

        return None

    def set_voxel_color(self, x: int, y: int, z: int, color: VoxelColor):
        self.dirty = True

        index = x + (z * 8) + (y * 64)

        self.color_table[index] = color.id


class VoxelEditor:
    game_controller: GameController = None

    world_x_min: int
    world_y_min: int
    world_z_min: int

    world_x_offset: int
    world_y_offset: int
    world_z_offset: int

    voxel_object_cache: dict[str, VoxelObject] = {}
    is_created_voxel_object: bool = False

    input_vector3: Vector3 = Vector3()
    output_error: wintypes.INT = wintypes.INT()
    output_width_depth_height: wintypes.UINT = wintypes.UINT()
    output_color_index: wintypes.BYTE = wintypes.BYTE()
    output_voxel_object_deleted: wintypes.BOOL = wintypes.BOOL()
    output_voxel_object_exists: wintypes.BOOL = wintypes.BOOL()
    output_voxel_object_property: VoxelObjectProperty = VoxelObjectProperty()

    def __init__(self, game: Game):
        self.game_controller = game.controller

        output_object_num_width = wintypes.DWORD()
        output_object_num_depth = wintypes.DWORD()
        output_object_num_height = wintypes.DWORD()
        output_aabb = AABB()

        self.game_controller.get_world_info(output_object_num_width, output_object_num_depth, output_object_num_height, output_aabb)

        self.world_x_min = output_aabb.min.x
        self.world_y_min = output_aabb.min.y
        self.world_z_min = output_aabb.min.z

        self.world_x_offset = self.world_x_min + VOXEL_OBJECT_HALF_SIZE
        self.world_y_offset = self.world_y_min + VOXEL_OBJECT_HALF_SIZE
        self.world_z_offset = self.world_z_min + VOXEL_OBJECT_HALF_SIZE

    def _get_voxel_object(self, x: int, y: int, z: int, create_if_not_exists: bool = True) -> VoxelObject | None:
        x = self.world_x_offset + (int((x - self.world_x_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)
        y = self.world_y_offset + (int((y - self.world_y_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)
        z = self.world_z_offset + (int((z - self.world_z_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)

        key = "%d_%d_%d" % (x, y, z)

        if key not in self.voxel_object_cache:
            voxel_object = None

            self.input_vector3.x = x
            self.input_vector3.y = y
            self.input_vector3.z = z

            voxel_object_lite = self.game_controller.get_voxel_object_with_float_coord(self.input_vector3)

            if voxel_object_lite is None:
                if not create_if_not_exists:
                    return None

                voxel_object_lite = self.game_controller.create_voxel_object(self.input_vector3, 8, 0, self.output_error)

                self.is_created_voxel_object = True

                if self.output_error.value != CREATE_VOXEL_OBJECT_ERROR_OK:
                    raise Exception("Failed to create voxel object. returned `{0}`".format(get_create_voxel_object_error_string(self.output_error.value)))

                voxel_object = VoxelObject(voxel_object_lite)
                voxel_object.clear()
            else:
                voxel_object = VoxelObject(voxel_object_lite)

            self.voxel_object_cache[key] = voxel_object
            return voxel_object

        return self.voxel_object_cache[key]

    def get_voxel(self, x: int, y: int, z: int) -> bool:
        voxel_object = self._get_voxel_object(x, y, z, False)

        if not voxel_object:
            return False

        x = int(x / VOXEL_OBJECT_8_SIZE) % 8
        y = int(y / VOXEL_OBJECT_8_SIZE) % 8
        z = int(z / VOXEL_OBJECT_8_SIZE) % 8

        return voxel_object.get_voxel(x, y, z)

    def set_voxel(self, x: int, y: int, z: int, value: bool):
        voxel_object = self._get_voxel_object(x, y, z, True)

        x = int(x / VOXEL_OBJECT_8_SIZE) % 8
        y = int(y / VOXEL_OBJECT_8_SIZE) % 8
        z = int(z / VOXEL_OBJECT_8_SIZE) % 8

        voxel_object.set_voxel(x, y, z, value)

    def set_voxel_with_color(self, x: int, y: int, z: int, value: bool, color: VoxelColor):
        voxel_object = self._get_voxel_object(x, y, z, True)

        x = int(x / VOXEL_OBJECT_8_SIZE) % 8
        y = int(y / VOXEL_OBJECT_8_SIZE) % 8
        z = int(z / VOXEL_OBJECT_8_SIZE) % 8

        voxel_object.set_voxel(x, y, z, value)
        voxel_object.set_voxel_color(x, y, z, color)

    def get_voxel_color(self, x: int, y: int, z: int) -> VoxelColor | None:
        voxel_object = self._get_voxel_object(x, y, z, False)

        if not voxel_object:
            return None

        x = int(x / VOXEL_OBJECT_8_SIZE) % 8
        y = int(y / VOXEL_OBJECT_8_SIZE) % 8
        z = int(z / VOXEL_OBJECT_8_SIZE) % 8

        return voxel_object.get_voxel_color(x, y, z)

    def set_voxel_color(self, x: int, y: int, z: int, color: VoxelColor) -> bool:
        voxel_object = self._get_voxel_object(x, y, z, False)

        if not voxel_object:
            return False

        x = int(x / VOXEL_OBJECT_8_SIZE) % 8
        y = int(y / VOXEL_OBJECT_8_SIZE) % 8
        z = int(z / VOXEL_OBJECT_8_SIZE) % 8

        voxel_object.set_voxel_color(x, y, z, color)

        return True

    def get_voxel_color_if_exists(self, x: int, y: int, z: int) -> VoxelColor | None:
        voxel_object = self._get_voxel_object(x, y, z, False)

        if not voxel_object:
            return None

        x = int(x / VOXEL_OBJECT_8_SIZE) % 8
        y = int(y / VOXEL_OBJECT_8_SIZE) % 8
        z = int(z / VOXEL_OBJECT_8_SIZE) % 8

        return voxel_object.get_voxel_color_if_exists(x, y, z)

    def finish(self):
        for voxel_object in self.voxel_object_cache.values():
            voxel_object.apply_tables()

        self.voxel_object_cache = {}
