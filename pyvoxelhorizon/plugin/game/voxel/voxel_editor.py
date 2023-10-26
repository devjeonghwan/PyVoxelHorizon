from ctypes import wintypes

from pyvoxelhorizon.enum import *
from pyvoxelhorizon.interface import *
from pyvoxelhorizon.plugin.game import *
from pyvoxelhorizon.struct import *
from .voxel_color import VoxelColor, get_voxel_color

VOXEL_OBJECT_SIZE = 400
VOXEL_OBJECT_8_SIZE = int(VOXEL_OBJECT_SIZE / 8)
VOXEL_OBJECT_HALF_SIZE = int(VOXEL_OBJECT_SIZE / 2)


def _align_voxel_object_8_coord(x: int) -> int:
    return int(x / VOXEL_OBJECT_8_SIZE) % 8


class VoxelEditor:
    game_controller: GameController = None

    world_x_min: int
    world_y_min: int
    world_z_min: int

    world_x_max: int
    world_y_max: int
    world_z_max: int

    voxel_object_cache: dict[str, VoxelObjectLite] = {}
    is_created_voxel_object: bool = False
    last_created_voxel_object: VoxelObjectLite | None = None

    input_vector3: Vector3 = Vector3()
    output_error: wintypes.INT = wintypes.INT()
    output_width_depth_height: wintypes.UINT = wintypes.UINT()
    output_color_index: wintypes.BYTE = wintypes.BYTE()
    output_voxel_object_deleted: wintypes.BOOL = wintypes.BOOL()
    output_voxel_object_exists: wintypes.BOOL = wintypes.BOOL()
    output_voxel_object_property: VoxelObjectProperty = VoxelObjectProperty()

    def __init__(self, game: Game):
        self.game_controller = game.game_controller

        output_object_num_width = wintypes.DWORD()
        output_object_num_depth = wintypes.DWORD()
        output_object_num_height = wintypes.DWORD()
        output_aabb = AABB()

        self.game_controller.get_world_info(output_object_num_width, output_object_num_depth, output_object_num_height, output_aabb)

        self.world_x_min = output_aabb.min.x
        self.world_y_min = output_aabb.min.y
        self.world_z_min = output_aabb.min.z

        self.world_x_max = output_aabb.max.x
        self.world_y_max = output_aabb.max.y
        self.world_z_max = output_aabb.max.z

    def _get_voxel_object(self, x: int, y: int, z: int, create_if_not_exists: bool = True) -> VoxelObjectLite | None:
        x = self.world_x_min + VOXEL_OBJECT_HALF_SIZE + (int((x - self.world_x_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)
        y = self.world_y_min + VOXEL_OBJECT_HALF_SIZE + (int((y - self.world_y_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)
        z = self.world_z_min + VOXEL_OBJECT_HALF_SIZE + (int((z - self.world_z_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)

        key = "{0}_{1}_{2}".format(x, y, z)

        self.input_vector3.x = x
        self.input_vector3.y = y
        self.input_vector3.z = z

        if key not in self.voxel_object_cache:
            voxel_object = self.game_controller.get_voxel_object_with_grid_coord(self.input_vector3)

            if not voxel_object:
                if not create_if_not_exists:
                    return None

                voxel_object = self.game_controller.create_voxel_object(self.input_vector3, 8, 0, self.output_error)
                self.is_created_voxel_object = True

                if self.output_error.value != CREATE_VOXEL_OBJECT_ERROR_OK:
                    raise Exception("Failed to create voxel object. returned `{0}`".format(get_create_voxel_object_error_string(self.output_error.value)))

                self.last_created_voxel_object = voxel_object

            self.voxel_object_cache[key] = voxel_object

        return self.voxel_object_cache[key]

    def _remove_voxel_object(self, x: int, y: int, z: int, remove_voxels: bool = True):
        x = self.world_x_min + VOXEL_OBJECT_HALF_SIZE + (int((x - self.world_x_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)
        y = self.world_y_min + VOXEL_OBJECT_HALF_SIZE + (int((y - self.world_y_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)
        z = self.world_z_min + VOXEL_OBJECT_HALF_SIZE + (int((z - self.world_z_min) / VOXEL_OBJECT_SIZE) * VOXEL_OBJECT_SIZE)

        key = "{0}_{1}_{2}".format(x, y, z)

        if key in self.voxel_object_cache:
            voxel_object = self.voxel_object_cache[key]

            if remove_voxels:
                voxel_object.remove_voxel_with_auto_resize(self.output_width_depth_height, self.output_voxel_object_deleted, 0, 0, 0, 1)

            del self.voxel_object_cache[key]

    def is_voxel_exists(self, x: int, y: int, z: int) -> bool:
        voxel_object = self._get_voxel_object(x, y, z, False)

        if not voxel_object:
            return False

        voxel_object.get_voxel_object_property(self.output_voxel_object_property)

        width_depth_height = self.output_voxel_object_property.width_depth_height

        scaled_x = int(width_depth_height * (_align_voxel_object_8_coord(x) / 8.0))
        scaled_y = int(width_depth_height * (_align_voxel_object_8_coord(y) / 8.0))
        scaled_z = int(width_depth_height * (_align_voxel_object_8_coord(z) / 8.0))

        if not voxel_object.get_voxel(self.output_voxel_object_exists, scaled_x, scaled_y, scaled_z):
            raise Exception("Unreachable Exception")

        return self.output_voxel_object_exists.value != 0

    def get_voxel_color(self, x: int, y: int, z: int) -> VoxelColor | None:
        voxel_object = self._get_voxel_object(x, y, z, False)

        if not voxel_object:
            return None

        voxel_object.get_voxel_object_property(self.output_voxel_object_property)

        width_depth_height = self.output_voxel_object_property.width_depth_height

        scaled_x = int(width_depth_height * (_align_voxel_object_8_coord(x) / 8.0))
        scaled_y = int(width_depth_height * (_align_voxel_object_8_coord(y) / 8.0))
        scaled_z = int(width_depth_height * (_align_voxel_object_8_coord(z) / 8.0))

        if not voxel_object.get_color_per_voxel(self.output_color_index, scaled_x, scaled_y, scaled_z):
            raise Exception("Unreachable Exception")

        return get_voxel_color(self.output_color_index.value)

    def set_voxel_color(self, x: int, y: int, z: int, color: VoxelColor) -> bool:
        voxel_object = self._get_voxel_object(x, y, z)

        x = _align_voxel_object_8_coord(x)
        y = _align_voxel_object_8_coord(y)
        z = _align_voxel_object_8_coord(z)

        return voxel_object.set_voxel_color_with_auto_resize(self.output_width_depth_height, x, y, z, color.id, 8)

    def add_voxel(self, x: int, y: int, z: int, color: VoxelColor) -> bool:
        voxel_object = self._get_voxel_object(x, y, z)

        x = _align_voxel_object_8_coord(x)
        y = _align_voxel_object_8_coord(y)
        z = _align_voxel_object_8_coord(z)

        if self.last_created_voxel_object == voxel_object:
            self.last_created_voxel_object = None
            return_value = voxel_object.clear_and_add_voxel(x, y, z, False)

            if not return_value:
                return False

            return voxel_object.set_voxel_color(x, y, z, color.id)

        return voxel_object.add_voxel_with_auto_resize(self.output_width_depth_height, x, y, z, color.id, 8)

    def remove_voxel(self, x: int, y: int, z: int) -> bool:
        voxel_object = self._get_voxel_object(x, y, z)

        voxel_x = _align_voxel_object_8_coord(x)
        voxel_y = _align_voxel_object_8_coord(y)
        voxel_z = _align_voxel_object_8_coord(z)

        return_value = voxel_object.remove_voxel_with_auto_resize(self.output_width_depth_height, self.output_voxel_object_deleted, voxel_x, voxel_y, voxel_z, 8)

        if self.output_voxel_object_deleted.value != 0:
            self._remove_voxel_object(x, y, z, remove_voxels=False)

        return return_value

    def finish(self):
        if self.is_created_voxel_object:
            for voxel_object in self.voxel_object_cache.values():
                voxel_object.update_geometry(False)
                voxel_object.update_lighting()

            self.is_created_voxel_object = False

        self.voxel_object_cache = {}
