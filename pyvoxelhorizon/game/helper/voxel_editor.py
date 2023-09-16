from pyvoxelhorizon.game.object import *

def _align_voxel_coord(value: float):
    return int(value / 50) % 8

class VoxelEditor:
    voxel_object_manager    : VoxelObjectManager        = None
    voxel_object_cache      : dict[str, VoxelObject]    = {}
    is_created_voxel_object : bool                      = False

    def __init__(self, voxel_object_manager: VoxelObjectManager):
        self.voxel_object_manager = voxel_object_manager
        self.voxel_object_cache = {}
        self.is_created_voxel_object = False
    
    def _get_voxel_object(self, x: int, y: int, z: int) -> VoxelObject:
        vector3 = Vector3()
        vector3.x = x
        vector3.y = y
        vector3.z = z

        align_vector3_to_voxel_object(vector3)

        key = str(int(vector3.x)) + "_" + str(int(vector3.y)) + "_" + str(int(vector3.z))

        if not key in self.voxel_object_cache:
            voxel_object = self.voxel_object_manager.get_voxel_object_with_float_coord(vector3)

            if not voxel_object:
                return None
            
            self.voxel_object_cache[key] = voxel_object

        return self.voxel_object_cache[key]
    
    def _remove_voxel_object(self, x: int, y: int, z: int):
        vector3 = Vector3()
        vector3.x = x
        vector3.y = y
        vector3.z = z

        align_vector3_to_voxel_object(vector3)

        key = str(int(vector3.x)) + "_" + str(int(vector3.y)) + "_" + str(int(vector3.z))

        if key in self.voxel_object_cache:
            del self.voxel_object_cache[key]
    
    def get_voxel(self, x: int, y: int, z: int) -> bool:
        voxel_object = self._get_voxel_object(x, y, z)

        if not voxel_object:
            return False
        
        voxel_object_property = voxel_object.get_voxel_object_property()
        width_depth_height = voxel_object_property.width_depth_height

        scaled_x = int(width_depth_height * (_align_voxel_coord(x) / 8))
        scaled_y = int(width_depth_height * (_align_voxel_coord(y) / 8))
        scaled_z = int(width_depth_height * (_align_voxel_coord(z) / 8))

        return voxel_object.get_voxel(scaled_x, scaled_y, scaled_z)
    
    def set_voxel_color(self, x: int, y: int, z: int, color: VoxelColor) -> bool:
        voxel_object = self._get_voxel_object(x, y, z)

        if not voxel_object:
            return False
        
        return voxel_object.set_voxel_color_with_auto_resize(8, _align_voxel_coord(x), _align_voxel_coord(y), _align_voxel_coord(z), color)
    
    def add_voxel(self, x: int, y: int, z: int, color: VoxelColor) -> bool:
        voxel_object = self._get_voxel_object(x, y, z)

        if not voxel_object:
            vector3 = Vector3()
            vector3.x = x
            vector3.y = y
            vector3.z = z

            result = self.voxel_object_manager.create_voxel_object(vector3, 8, 0)
    
            if not result.is_success():
                return False

            voxel_object = result.voxel_object

            voxel_object.update_geometry(False)
            voxel_object.update_lighting()

            if not voxel_object.clear_and_add_voxel(_align_voxel_coord(x), _align_voxel_coord(y), _align_voxel_coord(z), True):
                return False

            voxel_object.set_palette_with_indexed_color(color)
            
            return True
        
        return voxel_object.add_voxel_with_auto_resize(8, _align_voxel_coord(x), _align_voxel_coord(y), _align_voxel_coord(z), color)
    
    def remove_voxel(self, x: int, y: int, z: int) -> bool:
        voxel_object = self._get_voxel_object(x, y, z)

        if not voxel_object:
            return False
        
        if not voxel_object.remove_voxel_with_auto_resize(8, _align_voxel_coord(x), _align_voxel_coord(y), _align_voxel_coord(z)):
            return False
        
        self._remove_voxel_object(x, y, z)

        return True
    
    def finish(self):
        if self.is_created_voxel_object:
            self.voxel_object_manager.update_visibility()
        
        self.voxel_object_cache = {}