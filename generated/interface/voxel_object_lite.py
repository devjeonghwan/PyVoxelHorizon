import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enum import *
from pyvoxelhorizon.struct.voxel_object_property import VoxelObjectProperty
from pyvoxelhorizon.struct.int_vector3 import IntVector3
from pyvoxelhorizon.struct.aabb import AABB
from pyvoxelhorizon.struct.vector3 import Vector3

IS_FUNCTIONS_LOADED = False

FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PTR = None
FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_BODY_PTR = None
FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PROPERTY = None
FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_TABLE = None
FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE = None
FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE_WITH_STREAM = None
FUNCTION_VOXEL_OBJECT_LITE_SET_COMPRESSED_COLOR_TABLE2X2X2 = None
FUNCTION_VOXEL_OBJECT_LITE_SCLUPT_TO_ROUND_BOX = None
FUNCTION_VOXEL_OBJECT_LITE_SCULPT_TO_SPHERE = None
FUNCTION_VOXEL_OBJECT_LITE_UPDATE_GEOMETRY = None
FUNCTION_VOXEL_OBJECT_LITE_UPDATE_LIGHTING = None
FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL = None
FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_PER_VOXEL = None
FUNCTION_VOXEL_OBJECT_LITE_GET_FIRST_VOXEL_POS = None
FUNCTION_VOXEL_OBJECT_LITE_GET_AABB = None
FUNCTION_VOXEL_OBJECT_LITE_GET_BIT_TABLE = None
FUNCTION_VOXEL_OBJECT_LITE_SET_BIT_TABLE = None
FUNCTION_VOXEL_OBJECT_LITE_CLEAR_AND_ADD_VOXEL = None
FUNCTION_VOXEL_OBJECT_LITE_ADD_VOXEL_WITH_AUTO_RESIZE = None
FUNCTION_VOXEL_OBJECT_LITE_REMOVE_VOXEL_WITH_AUTO_RESIZE = None
FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR = None
FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR_WITH_AUTO_RESIZE = None
FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION = None
FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION_IN_GRID_SPACE = None
FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION = None
FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE = None
FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE_SPECIFY_DETAIL = None
FUNCTION_VOXEL_OBJECT_LITE_CALC_CENTER_POINT = None
FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_RANDOM = None
FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_INDEXED_COLOR = None
FUNCTION_VOXEL_OBJECT_LITE_GRADATION_COLOR_TABLE = None
FUNCTION_VOXEL_OBJECT_LITE_REPLACE_COLOR_INDEX = None
FUNCTION_VOXEL_OBJECT_LITE_RESIZE_WIDTH_DEPTH_HEIGHT = None
FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_GEOMETRY = None
FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_VOXELS = None
FUNCTION_VOXEL_OBJECT_LITE_SET_SELECTED = None
FUNCTION_VOXEL_OBJECT_LITE_CLEAR_SELECTED = None
FUNCTION_VOXEL_OBJECT_LITE_SET_DESTROYABLE = None
FUNCTION_VOXEL_OBJECT_LITE_IS_DESTROYABLE = None

def load_functions_of_voxel_object_lite(function_table_address: int):
    global IS_FUNCTIONS_LOADED
    
    if IS_FUNCTIONS_LOADED:
        return
    
    function_address = read_memory(function_table_address + 0, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PTR
    FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PTR = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 8, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_BODY_PTR
    FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_BODY_PTR = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 16, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PROPERTY
    FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PROPERTY = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 24, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_TABLE
    FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_TABLE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.UINT)(function_address)
    
    function_address = read_memory(function_table_address + 32, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE
    FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = read_memory(function_table_address + 40, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE_WITH_STREAM
    FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE_WITH_STREAM = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = read_memory(function_table_address + 48, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_COMPRESSED_COLOR_TABLE2X2X2
    FUNCTION_VOXEL_OBJECT_LITE_SET_COMPRESSED_COLOR_TABLE2X2X2 = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.UINT)(function_address)
    
    function_address = read_memory(function_table_address + 56, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SCLUPT_TO_ROUND_BOX
    FUNCTION_VOXEL_OBJECT_LITE_SCLUPT_TO_ROUND_BOX = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 64, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SCULPT_TO_SPHERE
    FUNCTION_VOXEL_OBJECT_LITE_SCULPT_TO_SPHERE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 72, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_UPDATE_GEOMETRY
    FUNCTION_VOXEL_OBJECT_LITE_UPDATE_GEOMETRY = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 80, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_UPDATE_LIGHTING
    FUNCTION_VOXEL_OBJECT_LITE_UPDATE_LIGHTING = ctypes.WINFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 88, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL
    FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)(function_address)
    
    function_address = read_memory(function_table_address + 96, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_PER_VOXEL
    FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_PER_VOXEL = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)(function_address)
    
    function_address = read_memory(function_table_address + 104, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_FIRST_VOXEL_POS
    FUNCTION_VOXEL_OBJECT_LITE_GET_FIRST_VOXEL_POS = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 112, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_AABB
    FUNCTION_VOXEL_OBJECT_LITE_GET_AABB = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 120, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_BIT_TABLE
    FUNCTION_VOXEL_OBJECT_LITE_GET_BIT_TABLE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 128, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_BIT_TABLE
    FUNCTION_VOXEL_OBJECT_LITE_SET_BIT_TABLE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 136, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_CLEAR_AND_ADD_VOXEL
    FUNCTION_VOXEL_OBJECT_LITE_CLEAR_AND_ADD_VOXEL = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 144, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_ADD_VOXEL_WITH_AUTO_RESIZE
    FUNCTION_VOXEL_OBJECT_LITE_ADD_VOXEL_WITH_AUTO_RESIZE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.BYTE, wintypes.UINT)(function_address)
    
    function_address = read_memory(function_table_address + 152, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_REMOVE_VOXEL_WITH_AUTO_RESIZE
    FUNCTION_VOXEL_OBJECT_LITE_REMOVE_VOXEL_WITH_AUTO_RESIZE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, wintypes.UINT)(function_address)
    
    function_address = read_memory(function_table_address + 160, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR
    FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.BYTE)(function_address)
    
    function_address = read_memory(function_table_address + 168, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR_WITH_AUTO_RESIZE
    FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR_WITH_AUTO_RESIZE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, ctypes.c_int, ctypes.c_int, wintypes.BYTE, wintypes.UINT)(function_address)
    
    function_address = read_memory(function_table_address + 176, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION
    FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 184, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION_IN_GRID_SPACE
    FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION_IN_GRID_SPACE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 192, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION
    FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)(function_address)
    
    function_address = read_memory(function_table_address + 200, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE
    FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 208, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE_SPECIFY_DETAIL
    FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE_SPECIFY_DETAIL = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT, ctypes.c_float)(function_address)
    
    function_address = read_memory(function_table_address + 216, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_CALC_CENTER_POINT
    FUNCTION_VOXEL_OBJECT_LITE_CALC_CENTER_POINT = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD)(function_address)
    
    function_address = read_memory(function_table_address + 224, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_RANDOM
    FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_RANDOM = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.DWORD)(function_address)
    
    function_address = read_memory(function_table_address + 232, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_INDEXED_COLOR
    FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_INDEXED_COLOR = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BYTE)(function_address)
    
    function_address = read_memory(function_table_address + 240, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_GRADATION_COLOR_TABLE
    FUNCTION_VOXEL_OBJECT_LITE_GRADATION_COLOR_TABLE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BYTE, wintypes.BYTE)(function_address)
    
    function_address = read_memory(function_table_address + 248, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_REPLACE_COLOR_INDEX
    FUNCTION_VOXEL_OBJECT_LITE_REPLACE_COLOR_INDEX = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BYTE, wintypes.BYTE)(function_address)
    
    function_address = read_memory(function_table_address + 256, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_RESIZE_WIDTH_DEPTH_HEIGHT
    FUNCTION_VOXEL_OBJECT_LITE_RESIZE_WIDTH_DEPTH_HEIGHT = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.UINT, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 264, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_GEOMETRY
    FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_GEOMETRY = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 272, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_VOXELS
    FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_VOXELS = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 280, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_SELECTED
    FUNCTION_VOXEL_OBJECT_LITE_SET_SELECTED = ctypes.WINFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 288, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_CLEAR_SELECTED
    FUNCTION_VOXEL_OBJECT_LITE_CLEAR_SELECTED = ctypes.WINFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = read_memory(function_table_address + 296, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_SET_DESTROYABLE
    FUNCTION_VOXEL_OBJECT_LITE_SET_DESTROYABLE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 304, ctypes.c_void_p)
    global FUNCTION_VOXEL_OBJECT_LITE_IS_DESTROYABLE
    FUNCTION_VOXEL_OBJECT_LITE_IS_DESTROYABLE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID)(function_address)
        
    IS_FUNCTIONS_LOADED = True

class VoxelObjectLite(AddressObject):
    def __init__(self, address: int):
        super().__init__(address)
        
        function_table_address = read_memory(address, ctypes.c_void_p)
        load_functions_of_voxel_object_lite(function_table_address)
    
    def get_voxel_object_ptr(self, pp_out_voxel_obj: int) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PTR(self.address, pp_out_voxel_obj)
    
    def get_voxel_object_body_ptr(self, pp_out_voxel_obj: int) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_BODY_PTR(self.address, pp_out_voxel_obj)
    
    def get_voxel_object_property(self, p_out_property: VoxelObjectProperty) -> None:
        p_out_property = get_address(p_out_property)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_OBJECT_PROPERTY(self.address, p_out_property)
    
    def get_color_table(self, p_out_color_table: wintypes.BYTE, dw_max_buffer_size: int, width_depth_height: int) -> bool:
        p_out_color_table = get_address(p_out_color_table)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_TABLE(self.address, p_out_color_table, dw_max_buffer_size, width_depth_height)
    
    def set_color_table(self, p_color_table: wintypes.BYTE, width_depth_height: int) -> bool:
        p_color_table = get_address(p_color_table)
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE(self.address, p_color_table, width_depth_height)
    
    def set_color_table_with_stream(self, p_color_table: wintypes.BYTE, width_depth_height: int) -> bool:
        p_color_table = get_address(p_color_table)
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_COLOR_TABLE_WITH_STREAM(self.address, p_color_table, width_depth_height)
    
    def set_compressed_color_table2x2x2(self, p_compressed_data: int, dw_size: int, width_depth_height: int) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_COMPRESSED_COLOR_TABLE2X2X2(self.address, p_compressed_data, dw_size, width_depth_height)
    
    def sclupt_to_round_box(self) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SCLUPT_TO_ROUND_BOX(self.address)
    
    def sculpt_to_sphere(self) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SCULPT_TO_SPHERE(self.address)
    
    def update_geometry(self, b_immediate: bool) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_UPDATE_GEOMETRY(self.address, b_immediate)
    
    def update_lighting(self) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_UPDATE_LIGHTING(self.address)
    
    def get_voxel(self, pb_out_value: wintypes.BOOL, x: int, y: int, z: int) -> bool:
        pb_out_value = get_address(pb_out_value)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL(self.address, pb_out_value, x, y, z)
    
    def get_color_per_voxel(self, pb_out_value: wintypes.BYTE, x: int, y: int, z: int) -> bool:
        pb_out_value = get_address(pb_out_value)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_COLOR_PER_VOXEL(self.address, pb_out_value, x, y, z)
    
    def get_first_voxel_pos(self, piv_out_voxel_pos: IntVector3) -> bool:
        piv_out_voxel_pos = get_address(piv_out_voxel_pos)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_FIRST_VOXEL_POS(self.address, piv_out_voxel_pos)
    
    def get_aabb(self, p_out_aabb: AABB) -> None:
        p_out_aabb = get_address(p_out_aabb)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_AABB(self.address, p_out_aabb)
    
    def get_bit_table(self, p_out_bit_table: ctypes.c_uint, dw_max_buffer_size: int, pui_out_width_depth_height: wintypes.UINT) -> bool:
        p_out_bit_table = get_address(p_out_bit_table)
        pui_out_width_depth_height = get_address(pui_out_width_depth_height)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_BIT_TABLE(self.address, p_out_bit_table, dw_max_buffer_size, pui_out_width_depth_height)
    
    def set_bit_table(self, p_bit_table: ctypes.c_uint, width_depth_height: int, b_immediate_update: bool) -> bool:
        p_bit_table = get_address(p_bit_table)
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_BIT_TABLE(self.address, p_bit_table, width_depth_height, b_immediate_update)
    
    def clear_and_add_voxel(self, x: int, y: int, z: int, b_immediate_update: bool) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_CLEAR_AND_ADD_VOXEL(self.address, x, y, z, b_immediate_update)
    
    def add_voxel_with_auto_resize(self, p_out_width_depth_height: wintypes.UINT, x: int, y: int, z: int, b_color_index: int, req_width_depth_height: int) -> bool:
        p_out_width_depth_height = get_address(p_out_width_depth_height)
        
        return FUNCTION_VOXEL_OBJECT_LITE_ADD_VOXEL_WITH_AUTO_RESIZE(self.address, p_out_width_depth_height, x, y, z, b_color_index, req_width_depth_height)
    
    def remove_voxel_with_auto_resize(self, p_out_width_depth_height: wintypes.UINT, pb_out_obj_deleted: wintypes.BOOL, x: int, y: int, z: int, req_width_depth_height: int) -> bool:
        p_out_width_depth_height = get_address(p_out_width_depth_height)
        pb_out_obj_deleted = get_address(pb_out_obj_deleted)
        
        return FUNCTION_VOXEL_OBJECT_LITE_REMOVE_VOXEL_WITH_AUTO_RESIZE(self.address, p_out_width_depth_height, pb_out_obj_deleted, x, y, z, req_width_depth_height)
    
    def set_voxel_color(self, x: int, y: int, z: int, b_color_index: int) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR(self.address, x, y, z, b_color_index)
    
    def set_voxel_color_with_auto_resize(self, p_out_width_depth_height: wintypes.UINT, x: int, y: int, z: int, b_color_index: int, req_width_depth_height: int) -> bool:
        p_out_width_depth_height = get_address(p_out_width_depth_height)
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_VOXEL_COLOR_WITH_AUTO_RESIZE(self.address, p_out_width_depth_height, x, y, z, b_color_index, req_width_depth_height)
    
    def get_position(self, pv3_out_pos: Vector3) -> None:
        pv3_out_pos = get_address(pv3_out_pos)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION(self.address, pv3_out_pos)
    
    def get_position_in_grid_space(self, piv_out_pos: IntVector3) -> None:
        piv_out_pos = get_address(piv_out_pos)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_POSITION_IN_GRID_SPACE(self.address, piv_out_pos)
    
    def get_voxel_position(self, pv3_out_pos: Vector3, x: int, y: int, z: int) -> bool:
        pv3_out_pos = get_address(pv3_out_pos)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION(self.address, pv3_out_pos, x, y, z)
    
    def get_voxel_position_in_obj_space(self, piv_out_pos: IntVector3, pv3_pos: Vector3) -> bool:
        piv_out_pos = get_address(piv_out_pos)
        pv3_pos = get_address(pv3_pos)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE(self.address, piv_out_pos, pv3_pos)
    
    def get_voxel_position_in_obj_space_specify_detail(self, piv_out_pos: IntVector3, pv3_pos: Vector3, width_depth_height: int, f_voxel_size: float) -> bool:
        piv_out_pos = get_address(piv_out_pos)
        pv3_pos = get_address(pv3_pos)
        
        return FUNCTION_VOXEL_OBJECT_LITE_GET_VOXEL_POSITION_IN_OBJ_SPACE_SPECIFY_DETAIL(self.address, piv_out_pos, pv3_pos, width_depth_height, f_voxel_size)
    
    def calc_center_point(self, pv3_out_point: Vector3, x: int, y: int, z: int) -> bool:
        pv3_out_point = get_address(pv3_out_point)
        
        return FUNCTION_VOXEL_OBJECT_LITE_CALC_CENTER_POINT(self.address, pv3_out_point, x, y, z)
    
    def set_palette_with_random(self, dw_max_color_num: int) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_RANDOM(self.address, dw_max_color_num)
    
    def set_palette_with_indexed_color(self, index: int) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_PALETTE_WITH_INDEXED_COLOR(self.address, index)
    
    def gradation_color_table(self, b_color_index: int, b_last_color_index: int) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_GRADATION_COLOR_TABLE(self.address, b_color_index, b_last_color_index)
    
    def replace_color_index(self, b_replace_index: int, b_comparand_index: int) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_REPLACE_COLOR_INDEX(self.address, b_replace_index, b_comparand_index)
    
    def resize_width_depth_height(self, width_depth_height: int, b_immediate_update: bool) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_RESIZE_WIDTH_DEPTH_HEIGHT(self.address, width_depth_height, b_immediate_update)
    
    def optimize_geometry(self) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_GEOMETRY(self.address)
    
    def optimize_voxels(self, b_immediate_update: bool) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_OPTIMIZE_VOXELS(self.address, b_immediate_update)
    
    def set_selected(self) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_SELECTED(self.address)
    
    def clear_selected(self) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_CLEAR_SELECTED(self.address)
    
    def set_destroyable(self, b_switch: bool) -> None:
        
        return FUNCTION_VOXEL_OBJECT_LITE_SET_DESTROYABLE(self.address, b_switch)
    
    def is_destroyable(self) -> bool:
        
        return FUNCTION_VOXEL_OBJECT_LITE_IS_DESTROYABLE(self.address)
    
