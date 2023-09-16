from .client_context import *

import ctypes
import ctypes.wintypes as wintypes
import struct

class VoxelColor:
    def __init__(self, id, rgb=None, description=None):
        self.id = id

        if rgb is None:
            self.rgb = None
        else:
            self.rgb = rgb

        if description is None:
            description = "RGB(" + str(self.rgb) + ")"

        self.description = description

VOXEL_COLORS = [
    VoxelColor(0, rgb=(71, 45, 60)),
    VoxelColor(1, rgb=(94, 54, 67)),
    VoxelColor(2, rgb=(122, 68, 74)),
    VoxelColor(3, rgb=(160, 91, 83)),
    VoxelColor(4, rgb=(191, 121, 88)),
    VoxelColor(5, rgb=(238, 161, 96)),
    VoxelColor(6, rgb=(244, 204, 161)),
    VoxelColor(7, rgb=(182, 213, 60)),
    VoxelColor(8, rgb=(113, 170, 52)),
    VoxelColor(9, rgb=(57, 123, 68)),
    VoxelColor(10, rgb=(60, 89, 86)),
    VoxelColor(11, rgb=(48, 44, 46)),
    VoxelColor(12, rgb=(90, 83, 83)),
    VoxelColor(13, rgb=(125, 112, 113)),
    VoxelColor(14, rgb=(160, 147, 142)),
    VoxelColor(15, rgb=(207, 198, 184)),

    VoxelColor(16, rgb=(223, 246, 245)),
    VoxelColor(17, rgb=(138, 235, 241)),
    VoxelColor(18, rgb=(40, 204, 223)),
    VoxelColor(19, rgb=(57, 120, 168)),
    VoxelColor(20, rgb=(57, 71, 120)),
    VoxelColor(21, rgb=(57, 49, 75)),
    VoxelColor(22, rgb=(86, 64, 100)),
    VoxelColor(23, rgb=(142, 71, 140)),
    VoxelColor(24, rgb=(205, 96, 147)),
    VoxelColor(25, rgb=(255, 174, 182)),
    VoxelColor(26, rgb=(244, 180, 27)),
    VoxelColor(27, rgb=(244, 126, 27)),
    VoxelColor(28, rgb=(230, 72, 46)),
    VoxelColor(29, rgb=(169, 59, 59)),
    VoxelColor(30, rgb=(130, 112, 148)),
    VoxelColor(31, rgb=(79, 84, 107)),

    VoxelColor(32, description="Green Grass"),
    VoxelColor(33, description="Dark Green Grass"),
    VoxelColor(34, description="Mud"),
    VoxelColor(35, description="Dirt1"),
    VoxelColor(36, description="Dirt2"),
    VoxelColor(37, description="Stone"),
    VoxelColor(38, description="Smooth Stone"),
    VoxelColor(39, description="Tile1"),
    VoxelColor(40, description="Tile2"),
    VoxelColor(41, description="Quartz"),
    VoxelColor(42, description="Blue Wool"),
    VoxelColor(43, description="Rock1"),
    VoxelColor(44, description="Rock2"),
    VoxelColor(45, description="Rock3"),
    VoxelColor(46, description="Check"),

    VoxelColor(47, description="Mat Green Grass"),
    VoxelColor(48, description="Mat Dark Green Grass"),
    VoxelColor(49, description="Mat Mud"),
    VoxelColor(50, description="Mat Dirt1"),
    VoxelColor(51, description="Mat Dirt2"),
    VoxelColor(52, description="Mat Stone"),
    VoxelColor(53, description="Mat Smooth Stone"),
    VoxelColor(54, description="Mat Tile1"),
    VoxelColor(55, description="Mat Tile2"),
    VoxelColor(56, description="Mat Quartz"),
    VoxelColor(57, description="Mat Blue Wool"),
    VoxelColor(58, description="Mat Rock1"),
    VoxelColor(59, description="Mat Rock2"),
    VoxelColor(60, description="Mat Rock3"),
    VoxelColor(61, description="Mat Check"),

    VoxelColor(62, description="Shining Check1"),
    VoxelColor(63, description="Shining Check2")
]
VOXEL_COLOR_RGB_CACHE = {}

def find_similar_voxel_color(red, green, blue):
    key = str(red) + "_" + str(green) + "_" + str(blue)

    if not key in VOXEL_COLOR_RGB_CACHE:
        find_distance = 255 * 255 * 255
        find_color = None

        for index in range(len(VOXEL_COLORS)):
            color = VOXEL_COLORS[index]

            if color.rgb != None:
                distance = (abs(color.rgb[0] - red) + abs(color.rgb[1] - green) + abs(color.rgb[2] - blue)) / 3

                if find_distance > distance:
                    find_distance = distance
                    find_color = color
                
        VOXEL_COLOR_RGB_CACHE[key] = find_color

    return VOXEL_COLOR_RGB_CACHE[key]

def get_voxel_color(index):
    if index > 0 or index <= len(VOXEL_COLORS):
        return VOXEL_COLORS[0]
    
    return VOXEL_COLORS[index]

class VoxelObjectProperty(ctypes.Structure):
    width_depth_height: int
    voxel_size: float

    _fields_ = (
        ('width_depth_height', ctypes.c_uint),
        ('voxel_size', ctypes.c_float)
    )

    def __repr__(self):
        return f'VoxelObjectProperty(width_depth_height={self.width_depth_height}, voxel_size={self.voxel_size})'

class VoxelObject:
    client_context          : ClientContext     = None
    address                 : int               = None
    
    function_update_geometry                    : ctypes.CFUNCTYPE  = None
    function_update_lighting                    : ctypes.CFUNCTYPE  = None

    function_get_voxel_object_property          : ctypes.CFUNCTYPE  = None

    function_get_voxel                          : ctypes.CFUNCTYPE  = None
    function_add_voxel_with_auto_resize         : ctypes.CFUNCTYPE  = None
    function_remove_voxel_with_auto_resize      : ctypes.CFUNCTYPE  = None
    function_clear_and_add_voxel                : ctypes.CFUNCTYPE  = None

    function_set_voxel_color_with_auto_resize   : ctypes.CFUNCTYPE  = None
    function_set_palette_with_indexed_color     : ctypes.CFUNCTYPE  = None
    
    function_set_destroyable                    : ctypes.CFUNCTYPE  = None
    function_is_destroyable                     : ctypes.CFUNCTYPE  = None

    def __init__(self, client_context: ClientContext, address: int):
        self.client_context = client_context
        self.address = address
        self.voxel_object_address = self.address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['OFFSET']

        voxel_object_function_table_address = read_memory(
            self.voxel_object_address,
            ctypes.c_void_p
        )
        
        function_update_geometry_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['UPDATE_GEOMETRY'], 
            ctypes.c_void_p
        )
        self.function_update_geometry = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_update_geometry_address)
        
        function_update_lighting_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['UPDATE_LIGHTING'], 
            ctypes.c_void_p
        )
        self.function_update_lighting = ctypes.CFUNCTYPE(None, wintypes.LPVOID)(function_update_lighting_address)
        

        function_get_voxel_object_property_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['GET_VOXEL_OBJECT_PROPERTY'], 
            ctypes.c_void_p
        )
        self.function_get_voxel_object_property = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_get_voxel_object_property_address)
        
        function_get_voxel_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['GET_VOXEL'], 
            ctypes.c_void_p
        )
        self.function_get_voxel = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG)(function_get_voxel_address)
        
        function_add_voxel_with_auto_resize_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['ADD_VOXEL_WITH_AUTO_RESIZE'], 
            ctypes.c_void_p
        )
        self.function_add_voxel_with_auto_resize = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.BYTE, wintypes.UINT)(function_add_voxel_with_auto_resize_address)
        
        function_remove_voxel_with_auto_resize_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['REMOVE_VOXEL_WITH_AUTO_RESIZE'], 
            ctypes.c_void_p
        )
        self.function_remove_voxel_with_auto_resize = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.UINT)(function_remove_voxel_with_auto_resize_address)

        function_clear_and_add_voxel_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['CLEAR_AND_ADD_VOXEL'], 
            ctypes.c_void_p
        )
        self.function_clear_and_add_voxel = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.UINT)(function_clear_and_add_voxel_address)

        
        function_set_voxel_color_with_auto_resize_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['SET_VOXEL_COLOR_WITH_AUTO_RESIZE'], 
            ctypes.c_void_p
        )
        self.function_set_voxel_color_with_auto_resize = ctypes.CFUNCTYPE(wintypes.INT, wintypes.LPVOID, wintypes.LPVOID, wintypes.ULONG, wintypes.ULONG, wintypes.ULONG, wintypes.BYTE, wintypes.UINT)(function_set_voxel_color_with_auto_resize_address)
        
        function_set_palette_with_indexed_color_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['SET_PALETTE_WITH_INDEXED_COLOR'], 
            ctypes.c_void_p
        )
        self.function_set_palette_with_indexed_color = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.UINT)(function_set_palette_with_indexed_color_address)
        

        function_set_destroyable_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['SET_DESTROYABLE'], 
            ctypes.c_void_p
        )
        self.function_set_destroyable = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_set_destroyable_address)
        
        function_is_destroyable_address = read_memory(
            voxel_object_function_table_address + VOXEL_OBJECT_OFFSET['VIRTUAL_FUNCTION_TABLE']['VOXEL_OBJECT']['FUNCTION']['IS_DESTROYABLE'], 
            ctypes.c_void_p
        )
        self.function_is_destroyable = ctypes.CFUNCTYPE(wintypes.BOOL, wintypes.LPVOID)(function_is_destroyable_address)
        
        
    def update_geometry(self, immediately: bool):
        self.function_update_geometry(self.voxel_object_address, immediately)

    def update_lighting(self):
        self.function_update_lighting(self.voxel_object_address)
    

    def get_voxel_object_property(self) -> VoxelObjectProperty:
        voxel_object_property = VoxelObjectProperty()

        self.function_get_voxel_object_property(self.voxel_object_address, ctypes.addressof(voxel_object_property))

        return voxel_object_property
    

    def get_voxel(self, x: int, y: int, z: int) -> bool:
        result = ctypes.c_int()

        return_value = self.function_get_voxel(self.voxel_object_address, ctypes.addressof(result), x, y, z)

        if return_value == 0:
            return False
        
        return result.value != 0
    
    def add_voxel_with_auto_resize(self, width_height_depth: int, x: int, y: int, z: int, color: VoxelColor) -> bool:
        dummy_width_height_depth = ctypes.c_int()

        return_value = self.function_add_voxel_with_auto_resize(self.voxel_object_address, ctypes.addressof(dummy_width_height_depth), x, y, z, color.id, width_height_depth)

        return return_value != 0
    
    def remove_voxel_with_auto_resize(self, width_height_depth: int, x: int, y: int, z: int) -> bool:
        dummy_width_height_depth = ctypes.c_int()
        dummy = ctypes.c_int()

        return_value = self.function_remove_voxel_with_auto_resize(self.voxel_object_address, ctypes.addressof(dummy_width_height_depth), ctypes.addressof(dummy), x, y, z, width_height_depth)

        return return_value != 0
    
    def clear_and_add_voxel(self, x: int, y: int, z: int, immediately_update: bool) -> bool:
        return_value = self.function_clear_and_add_voxel(self.voxel_object_address, x, y, z, immediately_update)

        return return_value != 0


    def set_voxel_color_with_auto_resize(self, width_height_depth: int, x: int, y: int, z: int, color: VoxelColor) -> bool:
        dummy_width_height_depth = ctypes.c_int()

        return_value = self.function_set_voxel_color_with_auto_resize(self.voxel_object_address, ctypes.addressof(dummy_width_height_depth), x, y, z, color.id, width_height_depth)

        return return_value != 0

    def set_palette_with_indexed_color(self, color: VoxelColor):
        self.function_set_palette_with_indexed_color(self.voxel_object_address, color.id)


    def set_destroyable(self, destroyable: bool):
        self.function_set_destroyable(self.voxel_object_address, destroyable)

    def is_destroyable(self):
        return self.function_is_destroyable(self.voxel_object_address) != 0
