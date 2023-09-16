from .client_context import *
from .voxel_color import *

import ctypes
import ctypes.wintypes as wintypes
import struct

class VoxelObjectProperty(ctypes.Structure):
    width_depth_height: int
    voxel_size: float

    _fields_ = (
        ('width_depth_height', ctypes.c_uint),
        ('voxel_size', ctypes.c_float)
    )

    def __repr__(self):
        return f'VoxelObjectProperty(width_depth_height={self.width_depth_height}, voxel_size={self.voxel_size})'

IS_FUNCTION_LOAD = False

FUNCTION_UPDATE_GEOMETRY = None
FUNCTION_UPDATE_LIGHTING = None

FUNCTION_GET_VOXEL_OBJECT_PROPERTY = None

FUNCTION_GET_VOXEL = None
FUNCTION_ADD_VOXEL_WITH_AUTO_RESIZE = None
FUNCTION_REMOVE_VOXEL_WITH_AUTO_RESIZE = None
FUNCTION_CLEAR_AND_ADD_VOXEL = None

FUNCTION_SET_VOXEL_COLOR_WITH_AUTO_RESIZE = None
FUNCTION_SET_PALETTE_WITH_INDEXED_COLOR = None

FUNCTION_SET_DESTROYABLE = None
FUNCTION_IS_DESTROYABLE = None

def load_functions(client_context: ClientContext, voxel_object_address: int):
    global IS_FUNCTION_LOAD
    
    if IS_FUNCTION_LOAD:
        return

    IS_FUNCTION_LOAD = True

    voxel_object_function_table_address = read_memory(
        voxel_object_address,
        ctypes.c_void_p
    )

    function_update_geometry_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['UPDATE_GEOMETRY'], 
        ctypes.c_void_p
    )
    global FUNCTION_UPDATE_GEOMETRY
    FUNCTION_UPDATE_GEOMETRY = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_update_geometry_address)
    
    function_update_lighting_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['UPDATE_LIGHTING'], 
        ctypes.c_void_p
    )
    global FUNCTION_UPDATE_LIGHTING
    FUNCTION_UPDATE_LIGHTING = ctypes.CFUNCTYPE(None, wintypes.LPVOID)(function_update_lighting_address)


    function_get_voxel_object_property_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['GET_VOXEL_OBJECT_PROPERTY'], 
        ctypes.c_void_p
    )
    global FUNCTION_GET_VOXEL_OBJECT_PROPERTY
    FUNCTION_GET_VOXEL_OBJECT_PROPERTY = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_get_voxel_object_property_address)
    
    
    function_get_voxel_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['GET_VOXEL'], 
        ctypes.c_void_p
    )
    global FUNCTION_GET_VOXEL
    FUNCTION_GET_VOXEL = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG)(function_get_voxel_address)

    function_add_voxel_with_auto_resize_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['ADD_VOXEL_WITH_AUTO_RESIZE'], 
        ctypes.c_void_p
    )
    global FUNCTION_ADD_VOXEL_WITH_AUTO_RESIZE
    FUNCTION_ADD_VOXEL_WITH_AUTO_RESIZE = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.BYTE, wintypes.UINT)(function_add_voxel_with_auto_resize_address)

    function_remove_voxel_with_auto_resize_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['REMOVE_VOXEL_WITH_AUTO_RESIZE'], 
        ctypes.c_void_p
    )
    global FUNCTION_REMOVE_VOXEL_WITH_AUTO_RESIZE
    FUNCTION_REMOVE_VOXEL_WITH_AUTO_RESIZE = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.UINT)(function_remove_voxel_with_auto_resize_address)

    function_clear_and_add_voxel_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['CLEAR_AND_ADD_VOXEL'], 
        ctypes.c_void_p
    )
    global FUNCTION_CLEAR_AND_ADD_VOXEL
    FUNCTION_CLEAR_AND_ADD_VOXEL = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.UINT)(function_clear_and_add_voxel_address)


    function_set_voxel_color_with_auto_resize_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['SET_VOXEL_COLOR_WITH_AUTO_RESIZE'], 
        ctypes.c_void_p
    )
    global FUNCTION_SET_VOXEL_COLOR_WITH_AUTO_RESIZE
    FUNCTION_SET_VOXEL_COLOR_WITH_AUTO_RESIZE = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.BYTE, wintypes.UINT)(function_set_voxel_color_with_auto_resize_address)
    
    function_set_palette_with_indexed_color_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['SET_PALETTE_WITH_INDEXED_COLOR'], 
        ctypes.c_void_p
    )
    global FUNCTION_SET_PALETTE_WITH_INDEXED_COLOR
    FUNCTION_SET_PALETTE_WITH_INDEXED_COLOR = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.UINT)(function_set_palette_with_indexed_color_address)

    
    function_set_destroyable_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['SET_DESTROYABLE'], 
        ctypes.c_void_p
    )
    global FUNCTION_SET_DESTROYABLE
    FUNCTION_SET_DESTROYABLE = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_set_destroyable_address)
    
    function_is_destroyable_address = read_memory(
        voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['IS_DESTROYABLE'], 
        ctypes.c_void_p
    )
    global FUNCTION_IS_DESTROYABLE
    FUNCTION_IS_DESTROYABLE = ctypes.CFUNCTYPE(wintypes.BOOL, wintypes.LPVOID)(function_is_destroyable_address)

class VoxelObject:
    client_context          : ClientContext     = None
    address                 : int               = None
    
    def __init__(self, client_context: ClientContext, address: int):
        self.client_context = client_context
        self.address = address
        self.voxel_object_address = self.address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['OFFSET']

        load_functions(client_context, self.voxel_object_address)
        
    def update_geometry(self, immediately: bool):
        FUNCTION_UPDATE_GEOMETRY(self.voxel_object_address, immediately)

    def update_lighting(self):
        FUNCTION_UPDATE_LIGHTING(self.voxel_object_address)
    

    def get_voxel_object_property(self) -> VoxelObjectProperty:
        voxel_object_property = VoxelObjectProperty()

        FUNCTION_GET_VOXEL_OBJECT_PROPERTY(self.voxel_object_address, ctypes.addressof(voxel_object_property))

        return voxel_object_property
    

    def get_voxel(self, x: int, y: int, z: int) -> bool:
        result = ctypes.c_int()

        return_value = FUNCTION_GET_VOXEL(self.voxel_object_address, ctypes.addressof(result), x, y, z)

        if return_value == 0:
            return False
        
        return result.value != 0
    
    def add_voxel_with_auto_resize(self, width_height_depth: int, x: int, y: int, z: int, color: VoxelColor) -> bool:
        dummy_width_height_depth = ctypes.c_int()

        return_value = FUNCTION_ADD_VOXEL_WITH_AUTO_RESIZE(self.voxel_object_address, ctypes.addressof(dummy_width_height_depth), x, y, z, color.id, width_height_depth)

        return return_value != 0
    
    def remove_voxel_with_auto_resize(self, width_height_depth: int, x: int, y: int, z: int) -> bool:
        dummy_width_height_depth = ctypes.c_int()
        dummy = ctypes.c_int()

        return_value = FUNCTION_REMOVE_VOXEL_WITH_AUTO_RESIZE(self.voxel_object_address, ctypes.addressof(dummy_width_height_depth), ctypes.addressof(dummy), x, y, z, width_height_depth)

        return return_value != 0
    
    def clear_and_add_voxel(self, x: int, y: int, z: int, immediately_update: bool) -> bool:
        return_value = FUNCTION_CLEAR_AND_ADD_VOXEL(self.voxel_object_address, x, y, z, immediately_update)

        return return_value != 0


    def set_voxel_color_with_auto_resize(self, width_height_depth: int, x: int, y: int, z: int, color: VoxelColor) -> bool:
        dummy_width_height_depth = ctypes.c_int()

        return_value = FUNCTION_SET_VOXEL_COLOR_WITH_AUTO_RESIZE(self.voxel_object_address, ctypes.addressof(dummy_width_height_depth), x, y, z, color.id, width_height_depth)

        return return_value != 0

    def set_palette_with_indexed_color(self, color: VoxelColor):
        FUNCTION_SET_PALETTE_WITH_INDEXED_COLOR(self.voxel_object_address, color.id)


    def set_destroyable(self, destroyable: bool):
        FUNCTION_SET_DESTROYABLE(self.voxel_object_address, destroyable)

    def is_destroyable(self):
        return FUNCTION_IS_DESTROYABLE(self.voxel_object_address) != 0
