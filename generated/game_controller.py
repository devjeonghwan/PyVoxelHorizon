import ctypes
import ctypes.wintypes as wintypes

IS_FUNCTIONS_LOADED = False

FUNCTION_GAME_CONTROLLER_GET_WORLD_INFO = None
FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT = None
FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT_OVERLOADED = None
FUNCTION_GAME_CONTROLLER_DELETE_VOXEL_OBJECT = None
FUNCTION_GAME_CONTROLLER_DELETE_ALL_VOXEL_OBJECT = None
FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_LIST_WITH_SPHERE = None
FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_WITH_FLOAT_COORD = None
FUNCTION_GAME_CONTROLLER_GET_FLOAT_POSITION_WITH_INT_COORD = None
FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AABB_WITH_INT_COORD = None
FUNCTION_GAME_CONTROLLER_INTERSECT_VOXEL_WITH_RAY_AS_TRI_MESH = None
FUNCTION_GAME_CONTROLLER_INTERSECT_BOTTOM_WITH_RAY = None
FUNCTION_GAME_CONTROLLER_FIND_TRI_LIST_WITH_CAPSULE_RAY = None
FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_GRID_COORD = None
FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_FLOAT_COORD = None
FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_NUM = None
FUNCTION_GAME_CONTROLLER_GET_PALETTED_COLOR_NUM = None
FUNCTION_GAME_CONTROLLER_SNAP_COORD = None
FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_POS = None
FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_POS = None
FUNCTION_GAME_CONTROLLER_SELECT_CURSOR_VOXEL_OBJECT_DETAIL = None
FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_SCALE = None
FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_VOXEL_SCALE = None
FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_RENDER_MODE = None
FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_PROPERY = None
FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_COLOR = None
FUNCTION_GAME_CONTROLLER_SET_BRUSH_VOXEL_OBJECT_COLOR = None
FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION = None
FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION_OVERLOADED = None
FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SPHERE = None
FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_CAPSULE = None
FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_AABB = None
FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SCREEN_RECT = None
FUNCTION_GAME_CONTROLLER_GET_PICEKD_POSITION = None
FUNCTION_GAME_CONTROLLER_ADD_VOXEL = None
FUNCTION_GAME_CONTROLLER_SET_VOXEL_COLOR = None
FUNCTION_GAME_CONTROLLER_GET_COLOR_TABLE_FROM_PALETTE = None
FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_AABB_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_AABB_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_AABB_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_SPHERE_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_SPHERE_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_BY_OBJ_LIST_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_BY_OBJ_LIST_AUTO_RESIZE = None
FUNCTION_GAME_CONTROLLER_WRITE_TEXT_TO_SYSTEM_DLG_W = None
FUNCTION_GAME_CONTROLLER_SET_FIRST_VOXEL_OBJECT = None
FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AND_NEXT = None
FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB = None
FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB_FOR_REMOVE = None
FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE = None
FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE_FOR_REMOVE = None
FUNCTION_GAME_CONTROLLER_GET_FOOTREST_BASE_OBJ_POS = None
FUNCTION_GAME_CONTROLLER_GET_FOOTREST_QUAD_LIST = None
FUNCTION_GAME_CONTROLLER_GET_FOOTREST_HEIGHT = None
FUNCTION_GAME_CONTROLLER_SET_SELECTED_VOXEL = None
FUNCTION_GAME_CONTROLLER_SET_SELECTED = None
FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_VOXEL = None
FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_ALL = None
FUNCTION_GAME_CONTROLLER_WRITE_FILE = None
FUNCTION_GAME_CONTROLLER_READ_FILE = None
FUNCTION_GAME_CONTROLLER_GET_CURRENT_COLOR_INDEX = None
FUNCTION_GAME_CONTROLLER_GET_CURRENT_EDIT_MODE = None
FUNCTION_GAME_CONTROLLER_GET_CURRENT_PLANE_TYPE = None
FUNCTION_GAME_CONTROLLER_GET_SELECTED_VOXEL_OBJ_DESC = None
FUNCTION_GAME_CONTROLLER_GET_CURSOR_STATUS = None
FUNCTION_GAME_CONTROLLER_IS_UPDATING = None
FUNCTION_GAME_CONTROLLER_UPDATE_VISIBILITY_ALL = None
FUNCTION_GAME_CONTROLLER_ENABLE_DESTROYABLE_ALL = None
FUNCTION_GAME_CONTROLLER_ENABLE_AUTO_RESTORE_ALL = None

def load_functions_of_game_controller(function_table_address: int):
    global IS_FUNCTIONS_LOADED
    
    if IS_FUNCTIONS_LOADED:
        return
    
    function_address = ctypes.cast(function_table_address + 0, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_WORLD_INFO
    FUNCTION_GAME_CONTROLLER_GET_WORLD_INFO = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 8, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT
    FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT = ctypes.WINFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.DWORD, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 16, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT_OVERLOADED
    FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT_OVERLOADED = ctypes.WINFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.BOOL, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 24, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_DELETE_VOXEL_OBJECT
    FUNCTION_GAME_CONTROLLER_DELETE_VOXEL_OBJECT = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 32, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_DELETE_ALL_VOXEL_OBJECT
    FUNCTION_GAME_CONTROLLER_DELETE_ALL_VOXEL_OBJECT = ctypes.WINFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 40, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_LIST_WITH_SPHERE
    FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_LIST_WITH_SPHERE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 48, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_WITH_FLOAT_COORD
    FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_WITH_FLOAT_COORD = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 56, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_FLOAT_POSITION_WITH_INT_COORD
    FUNCTION_GAME_CONTROLLER_GET_FLOAT_POSITION_WITH_INT_COORD = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 64, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AABB_WITH_INT_COORD
    FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AABB_WITH_INT_COORD = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 72, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_INTERSECT_VOXEL_WITH_RAY_AS_TRI_MESH
    FUNCTION_GAME_CONTROLLER_INTERSECT_VOXEL_WITH_RAY_AS_TRI_MESH = ctypes.WINFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 80, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_INTERSECT_BOTTOM_WITH_RAY
    FUNCTION_GAME_CONTROLLER_INTERSECT_BOTTOM_WITH_RAY = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 88, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_FIND_TRI_LIST_WITH_CAPSULE_RAY
    FUNCTION_GAME_CONTROLLER_FIND_TRI_LIST_WITH_CAPSULE_RAY = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 96, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_GRID_COORD
    FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_GRID_COORD = ctypes.WINFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 104, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_FLOAT_COORD
    FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_FLOAT_COORD = ctypes.WINFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 112, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_NUM
    FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_NUM = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 120, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_PALETTED_COLOR_NUM
    FUNCTION_GAME_CONTROLLER_GET_PALETTED_COLOR_NUM = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 128, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SNAP_COORD
    FUNCTION_GAME_CONTROLLER_SNAP_COORD = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 136, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_POS
    FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_POS = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 144, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_POS
    FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_POS = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 152, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SELECT_CURSOR_VOXEL_OBJECT_DETAIL
    FUNCTION_GAME_CONTROLLER_SELECT_CURSOR_VOXEL_OBJECT_DETAIL = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 160, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_SCALE
    FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_SCALE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, ctypes.c_float)(function_address)
    
    function_address = ctypes.cast(function_table_address + 168, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_VOXEL_SCALE
    FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_VOXEL_SCALE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, ctypes.c_float)(function_address)
    
    function_address = ctypes.cast(function_table_address + 176, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_RENDER_MODE
    FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_RENDER_MODE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, ctypes.c_int)(function_address)
    
    function_address = ctypes.cast(function_table_address + 184, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_PROPERY
    FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_PROPERY = ctypes.WINFUNCTYPE(wintypes.UINT, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 192, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_COLOR
    FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_COLOR = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 200, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_BRUSH_VOXEL_OBJECT_COLOR
    FUNCTION_GAME_CONTROLLER_SET_BRUSH_VOXEL_OBJECT_COLOR = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 208, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION
    FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 216, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION_OVERLOADED
    FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION_OVERLOADED = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 224, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SPHERE
    FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SPHERE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 232, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_CAPSULE
    FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_CAPSULE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 240, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_AABB
    FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_AABB = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 248, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SCREEN_RECT
    FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SCREEN_RECT = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, wintypes.LPVOID, ctypes.c_float, wintypes.DWORD, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 256, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_PICEKD_POSITION
    FUNCTION_GAME_CONTROLLER_GET_PICEKD_POSITION = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 264, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_ADD_VOXEL
    FUNCTION_GAME_CONTROLLER_ADD_VOXEL = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE, wintypes.BOOL, wintypes.BOOL)(function_address)
    
    function_address = ctypes.cast(function_table_address + 272, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_VOXEL_COLOR
    FUNCTION_GAME_CONTROLLER_SET_VOXEL_COLOR = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE, wintypes.BOOL)(function_address)
    
    function_address = ctypes.cast(function_table_address + 280, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_COLOR_TABLE_FROM_PALETTE
    FUNCTION_GAME_CONTROLLER_GET_COLOR_TABLE_FROM_PALETTE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 288, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_AABB_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_AABB_AUTO_RESIZE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 296, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_AABB_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_AABB_AUTO_RESIZE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 304, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_AABB_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_AABB_AUTO_RESIZE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 312, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_SPHERE_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_SPHERE_AUTO_RESIZE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.LPVOID, wintypes.UINT, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 320, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_SPHERE_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_SPHERE_AUTO_RESIZE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.LPVOID, wintypes.UINT, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 328, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_AUTO_RESIZE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 336, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_BY_OBJ_LIST_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_BY_OBJ_LIST_AUTO_RESIZE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.LPVOID, wintypes.DWORD, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 344, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_AUTO_RESIZE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 352, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_BY_OBJ_LIST_AUTO_RESIZE
    FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_BY_OBJ_LIST_AUTO_RESIZE = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float, wintypes.LPVOID, wintypes.DWORD, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 360, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_WRITE_TEXT_TO_SYSTEM_DLG_W
    FUNCTION_GAME_CONTROLLER_WRITE_TEXT_TO_SYSTEM_DLG_W = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.DWORD, ctypes.c_wchar_p)(function_address)
    
    function_address = ctypes.cast(function_table_address + 368, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_FIRST_VOXEL_OBJECT
    FUNCTION_GAME_CONTROLLER_SET_FIRST_VOXEL_OBJECT = ctypes.WINFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 376, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AND_NEXT
    FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AND_NEXT = ctypes.WINFUNCTYPE(wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 384, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB
    FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 392, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB_FOR_REMOVE
    FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB_FOR_REMOVE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 400, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE
    FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 408, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE_FOR_REMOVE
    FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE_FOR_REMOVE = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT)(function_address)
    
    function_address = ctypes.cast(function_table_address + 416, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_FOOTREST_BASE_OBJ_POS
    FUNCTION_GAME_CONTROLLER_GET_FOOTREST_BASE_OBJ_POS = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_float)(function_address)
    
    function_address = ctypes.cast(function_table_address + 424, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_FOOTREST_QUAD_LIST
    FUNCTION_GAME_CONTROLLER_GET_FOOTREST_QUAD_LIST = ctypes.WINFUNCTYPE(wintypes.DWORD, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPVOID, ctypes.c_int, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 432, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_FOOTREST_HEIGHT
    FUNCTION_GAME_CONTROLLER_GET_FOOTREST_HEIGHT = ctypes.WINFUNCTYPE(ctypes.c_float, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 440, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_SELECTED_VOXEL
    FUNCTION_GAME_CONTROLLER_SET_SELECTED_VOXEL = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, ctypes.c_int, ctypes.c_int)(function_address)
    
    function_address = ctypes.cast(function_table_address + 448, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_SET_SELECTED
    FUNCTION_GAME_CONTROLLER_SET_SELECTED = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 456, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_VOXEL
    FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_VOXEL = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, ctypes.c_int, ctypes.c_int, ctypes.c_int)(function_address)
    
    function_address = ctypes.cast(function_table_address + 464, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_ALL
    FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_ALL = ctypes.WINFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 472, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_WRITE_FILE
    FUNCTION_GAME_CONTROLLER_WRITE_FILE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, ctypes.c_wchar_p)(function_address)
    
    function_address = ctypes.cast(function_table_address + 480, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_READ_FILE
    FUNCTION_GAME_CONTROLLER_READ_FILE = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, ctypes.c_wchar_p, wintypes.BOOL, wintypes.BOOL)(function_address)
    
    function_address = ctypes.cast(function_table_address + 488, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_CURRENT_COLOR_INDEX
    FUNCTION_GAME_CONTROLLER_GET_CURRENT_COLOR_INDEX = ctypes.WINFUNCTYPE(wintypes.BYTE, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 496, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_CURRENT_EDIT_MODE
    FUNCTION_GAME_CONTROLLER_GET_CURRENT_EDIT_MODE = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 504, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_CURRENT_PLANE_TYPE
    FUNCTION_GAME_CONTROLLER_GET_CURRENT_PLANE_TYPE = ctypes.WINFUNCTYPE(ctypes.c_int, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 512, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_SELECTED_VOXEL_OBJ_DESC
    FUNCTION_GAME_CONTROLLER_GET_SELECTED_VOXEL_OBJ_DESC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 520, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_GET_CURSOR_STATUS
    FUNCTION_GAME_CONTROLLER_GET_CURSOR_STATUS = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 528, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_IS_UPDATING
    FUNCTION_GAME_CONTROLLER_IS_UPDATING = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 536, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_UPDATE_VISIBILITY_ALL
    FUNCTION_GAME_CONTROLLER_UPDATE_VISIBILITY_ALL = ctypes.WINFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 544, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_ENABLE_DESTROYABLE_ALL
    FUNCTION_GAME_CONTROLLER_ENABLE_DESTROYABLE_ALL = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_address)
    
    function_address = ctypes.cast(function_table_address + 552, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_GAME_CONTROLLER_ENABLE_AUTO_RESTORE_ALL
    FUNCTION_GAME_CONTROLLER_ENABLE_AUTO_RESTORE_ALL = ctypes.WINFUNCTYPE(None, wintypes.LPVOID, wintypes.BOOL)(function_address)
        
    IS_FUNCTIONS_LOADED = True

class GameController:
    address: int = None
    
    def __init__(self, address: int):
        self.address = address
        
        function_table_address = ctypes.cast(address, ctypes.POINTER(ctypes.c_void_p))[0]
        load_functions_of_game_controller(function_table_address)
    
    def get_world_info(self, pdw_out_obj_num_width: int, pdw_out_obj_num_depth: int, pdw_out_obj_num_height: int, p_out_world_aabb: int) -> None:
        FUNCTION_GAME_CONTROLLER_GET_WORLD_INFO(self.address, pdw_out_obj_num_width, pdw_out_obj_num_depth, pdw_out_obj_num_height, p_out_world_aabb)
    
    def create_voxel_object(self, pv3_pos: int, dw_width_depth_height: int, color: int, p_out_err: int) -> int:
        return FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT(self.address, pv3_pos, dw_width_depth_height, color, p_out_err)
    
    def create_voxel_object_overloaded(self, piv3_pos_in_grid_space: int, dw_width_depth_height: int, p_bit_table: int, p_color_table: int, color: int, b_immdieate_update: bool, p_out_err: int) -> int:
        return FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_OBJECT_OVERLOADED(self.address, piv3_pos_in_grid_space, dw_width_depth_height, p_bit_table, p_color_table, color, b_immdieate_update, p_out_err)
    
    def delete_voxel_object(self, p_voxel_obj_lite: int) -> None:
        FUNCTION_GAME_CONTROLLER_DELETE_VOXEL_OBJECT(self.address, p_voxel_obj_lite)
    
    def delete_all_voxel_object(self) -> None:
        FUNCTION_GAME_CONTROLLER_DELETE_ALL_VOXEL_OBJECT(self.address)
    
    def get_int_position_list_with_sphere(self, piv_out_pos_list: int, dw_max_pos_count: int, p_bs: int, pb_out_insufficient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_LIST_WITH_SPHERE(self.address, piv_out_pos_list, dw_max_pos_count, p_bs, pb_out_insufficient)
    
    def get_int_position_with_float_coord(self, piv_out_pos: int, pv3_pos: int) -> None:
        FUNCTION_GAME_CONTROLLER_GET_INT_POSITION_WITH_FLOAT_COORD(self.address, piv_out_pos, pv3_pos)
    
    def get_float_position_with_int_coord(self, pv3_out_pos: int, piv_pos: int) -> None:
        FUNCTION_GAME_CONTROLLER_GET_FLOAT_POSITION_WITH_INT_COORD(self.address, pv3_out_pos, piv_pos)
    
    def get_voxel_object_aabb_with_int_coord(self, p_out_aabb: int, piv_pos: int) -> None:
        FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AABB_WITH_INT_COORD(self.address, p_out_aabb, piv_pos)
    
    def intersect_voxel_with_ray_as_tri_mesh(self, pv3_out_intersect_point: int, pf_out_t: int, pv3_orig: int, pv3_ray: int) -> int:
        return FUNCTION_GAME_CONTROLLER_INTERSECT_VOXEL_WITH_RAY_AS_TRI_MESH(self.address, pv3_out_intersect_point, pf_out_t, pv3_orig, pv3_ray)
    
    def intersect_bottom_with_ray(self, pv3_out_intersect_point: int, pv3_orig: int, pv3_ray: int) -> bool:
        return FUNCTION_GAME_CONTROLLER_INTERSECT_BOTTOM_WITH_RAY(self.address, pv3_out_intersect_point, pv3_orig, pv3_ray)
    
    def find_tri_list_with_capsule_ray(self, p_out_tri_list: int, i_max_tri_num: int, pv3_orig: int, pv3_ray: int, f_rs: float, pb_out_insufficient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_FIND_TRI_LIST_WITH_CAPSULE_RAY(self.address, p_out_tri_list, i_max_tri_num, pv3_orig, pv3_ray, f_rs, pb_out_insufficient)
    
    def get_voxel_object_with_grid_coord(self, piv_pos: int) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_GRID_COORD(self.address, piv_pos)
    
    def get_voxel_object_with_float_coord(self, pv3_pos: int) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_WITH_FLOAT_COORD(self.address, pv3_pos)
    
    def get_voxel_object_num(self) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_NUM(self.address)
    
    def get_paletted_color_num(self) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_PALETTED_COLOR_NUM(self.address)
    
    def snap_coord(self, pv3_out_snapped_pos: int, pv3_pos: int) -> None:
        FUNCTION_GAME_CONTROLLER_SNAP_COORD(self.address, pv3_out_snapped_pos, pv3_pos)
    
    def set_cursor_voxel_object_pos(self, pv3_pos: int, b_select_voxel: bool, pv3_picked_pos: int, pv3_normal: int) -> None:
        FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_POS(self.address, pv3_pos, b_select_voxel, pv3_picked_pos, pv3_normal)
    
    def get_cursor_voxel_object_pos(self, pv3_out_pos: int, piv3_out_voxel_pos: int) -> None:
        FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_POS(self.address, pv3_out_pos, piv3_out_voxel_pos)
    
    def select_cursor_voxel_object_detail(self, width_depth_height: int) -> None:
        FUNCTION_GAME_CONTROLLER_SELECT_CURSOR_VOXEL_OBJECT_DETAIL(self.address, width_depth_height)
    
    def set_cursor_voxel_object_scale(self, f_obj_scale: float) -> None:
        FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_SCALE(self.address, f_obj_scale)
    
    def set_cursor_voxel_object_voxel_scale(self, f_voxel_scale: float) -> None:
        FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_VOXEL_SCALE(self.address, f_voxel_scale)
    
    def set_cursor_voxel_object_render_mode(self, mode: int) -> None:
        FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_RENDER_MODE(self.address, mode)
    
    def get_cursor_voxel_object_propery(self, pf_out_voxel_size: int) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_CURSOR_VOXEL_OBJECT_PROPERY(self.address, pf_out_voxel_size)
    
    def set_cursor_voxel_object_color(self, b_color_index: int) -> None:
        FUNCTION_GAME_CONTROLLER_SET_CURSOR_VOXEL_OBJECT_COLOR(self.address, b_color_index)
    
    def set_brush_voxel_object_color(self, b_color_index: int) -> None:
        FUNCTION_GAME_CONTROLLER_SET_BRUSH_VOXEL_OBJECT_COLOR(self.address, b_color_index)
    
    def is_valid_voxel_object_position(self, pv3_pos: int) -> bool:
        return FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION(self.address, pv3_pos)
    
    def is_valid_voxel_object_position_overloaded(self, piv_pos: int) -> bool:
        return FUNCTION_GAME_CONTROLLER_IS_VALID_VOXEL_OBJECT_POSITION_OVERLOADED(self.address, piv_pos)
    
    def find_voxel_object_list_with_sphere(self, pp_out_voxel_obj_lite_list: int, i_max_buffer_count: int, p_bs: int, pb_out_insufficient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SPHERE(self.address, pp_out_voxel_obj_lite_list, i_max_buffer_count, p_bs, pb_out_insufficient)
    
    def find_voxel_object_list_with_capsule(self, pp_out_voxel_obj_lite_list: int, i_max_buffer_count: int, pv3_ray_orig: int, pv3_ray_dir: int, f_rs: float, pb_out_insufficient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_CAPSULE(self.address, pp_out_voxel_obj_lite_list, i_max_buffer_count, pv3_ray_orig, pv3_ray_dir, f_rs, pb_out_insufficient)
    
    def find_voxel_object_list_with_aabb(self, pp_out_voxel_obj_lite_list: int, i_max_buffer_count: int, p_aabb: int, pb_out_insufficient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_AABB(self.address, pp_out_voxel_obj_lite_list, i_max_buffer_count, p_aabb, pb_out_insufficient)
    
    def find_voxel_object_list_with_screen_rect(self, pp_out_voxel_obj_lite_list: int, i_max_buffer_count: int, p_rect: int, f_dist: float, dw_viewport_index: int, pb_out_insufficient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_FIND_VOXEL_OBJECT_LIST_WITH_SCREEN_RECT(self.address, pp_out_voxel_obj_lite_list, i_max_buffer_count, p_rect, f_dist, dw_viewport_index, pb_out_insufficient)
    
    def get_picekd_position(self, pv3_out_pos: int, pv3_out_picked_axis: int, pf_out_dist: int) -> bool:
        return FUNCTION_GAME_CONTROLLER_GET_PICEKD_POSITION(self.address, pv3_out_pos, pv3_out_picked_axis, pf_out_dist)
    
    def add_voxel(self, pv3_cursor_obj_pos: int, piv_cursor_voxel_pos: int, b_color_index: int, b_recursive_plane: bool, b_rebuild_area: bool) -> bool:
        return FUNCTION_GAME_CONTROLLER_ADD_VOXEL(self.address, pv3_cursor_obj_pos, piv_cursor_voxel_pos, b_color_index, b_recursive_plane, b_rebuild_area)
    
    def set_voxel_color(self, p_voxel_obj: int, pv3_cursor_obj_pos: int, piv_cursor_voxel_pos: int, b_color_index: int, b_recursive_plane: bool) -> bool:
        return FUNCTION_GAME_CONTROLLER_SET_VOXEL_COLOR(self.address, p_voxel_obj, pv3_cursor_obj_pos, piv_cursor_voxel_pos, b_color_index, b_recursive_plane)
    
    def get_color_table_from_palette(self, pdw_out_color_table: int, dw_max_buffer_count: int, pb_out_insufficient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_COLOR_TABLE_FROM_PALETTE(self.address, pdw_out_color_table, dw_max_buffer_count, pb_out_insufficient)
    
    def add_voxels_with_aabb_auto_resize(self, p_aabb: int, p_clip_plane: int, width_depth_height: int, b_color_index: int) -> int:
        return FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_AABB_AUTO_RESIZE(self.address, p_aabb, p_clip_plane, width_depth_height, b_color_index)
    
    def paint_voxels_with_aabb_auto_resize(self, p_aabb: int, width_depth_height: int, b_color_index: int) -> None:
        FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_AABB_AUTO_RESIZE(self.address, p_aabb, width_depth_height, b_color_index)
    
    def remove_voxels_with_aabb_auto_resize(self, p_aabb: int, width_depth_height: int) -> None:
        FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_AABB_AUTO_RESIZE(self.address, p_aabb, width_depth_height)
    
    def add_voxels_with_sphere_auto_resize(self, pv3_pos: int, f_rs: float, p_clip_plane: int, width_depth_height: int, b_color_index: int) -> int:
        return FUNCTION_GAME_CONTROLLER_ADD_VOXELS_WITH_SPHERE_AUTO_RESIZE(self.address, pv3_pos, f_rs, p_clip_plane, width_depth_height, b_color_index)
    
    def paint_voxels_with_sphere_auto_resize(self, pv3_pos: int, f_rs: float, p_clip_plane: int, width_depth_height: int, b_color_index: int) -> None:
        FUNCTION_GAME_CONTROLLER_PAINT_VOXELS_WITH_SPHERE_AUTO_RESIZE(self.address, pv3_pos, f_rs, p_clip_plane, width_depth_height, b_color_index)
    
    def remove_voxels_with_sphere_auto_resize(self, pv3_pos: int, f_rs: float, width_depth_height: int) -> None:
        FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_AUTO_RESIZE(self.address, pv3_pos, f_rs, width_depth_height)
    
    def remove_voxels_with_sphere_by_obj_list_auto_resize(self, pv3_pos: int, f_rs: float, pv3_obj_list: int, dw_obj_num: int, width_depth_height: int) -> None:
        FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_SPHERE_BY_OBJ_LIST_AUTO_RESIZE(self.address, pv3_pos, f_rs, pv3_obj_list, dw_obj_num, width_depth_height)
    
    def remove_voxels_with_capsule_auto_resize(self, pv3_ray_orig: int, pv3_ray_dir: int, f_rs: float, width_depth_height: int) -> None:
        FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_AUTO_RESIZE(self.address, pv3_ray_orig, pv3_ray_dir, f_rs, width_depth_height)
    
    def remove_voxels_with_capsule_by_obj_list_auto_resize(self, pv3_ray_orig: int, pv3_ray_dir: int, f_rs: float, pv3_obj_list: int, dw_obj_num: int, width_depth_height: int) -> None:
        FUNCTION_GAME_CONTROLLER_REMOVE_VOXELS_WITH_CAPSULE_BY_OBJ_LIST_AUTO_RESIZE(self.address, pv3_ray_orig, pv3_ray_dir, f_rs, pv3_obj_list, dw_obj_num, width_depth_height)
    
    def write_text_to_system_dlg_w(self, dw_color: int, *args) -> None:
        FUNCTION_GAME_CONTROLLER_WRITE_TEXT_TO_SYSTEM_DLG_W(self.address, dw_color, *args)
    
    def set_first_voxel_object(self) -> None:
        FUNCTION_GAME_CONTROLLER_SET_FIRST_VOXEL_OBJECT(self.address)
    
    def get_voxel_object_and_next(self) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_VOXEL_OBJECT_AND_NEXT(self.address)
    
    def create_voxel_point_list_with_world_aabb(self, pv3_out_point_list: int, dw_max_buffer_count: int, p_aabb: int, p_clip_plane: int, width_depth_height: int) -> int:
        return FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB(self.address, pv3_out_point_list, dw_max_buffer_count, p_aabb, p_clip_plane, width_depth_height)
    
    def create_voxel_point_list_with_world_aabb_for_remove(self, pv3_out_point_list: int, dw_max_buffer_count: int, p_aabb: int, p_clip_plane: int, width_depth_height: int) -> int:
        return FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_AABB_FOR_REMOVE(self.address, pv3_out_point_list, dw_max_buffer_count, p_aabb, p_clip_plane, width_depth_height)
    
    def create_voxel_point_list_with_world_sphere(self, pv3_out_point_list: int, dw_max_buffer_count: int, p_bs: int, p_clip_plane: int, width_depth_height: int) -> int:
        return FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE(self.address, pv3_out_point_list, dw_max_buffer_count, p_bs, p_clip_plane, width_depth_height)
    
    def create_voxel_point_list_with_world_sphere_for_remove(self, pv3_out_point_list: int, dw_max_buffer_count: int, p_bs: int, p_clip_plane: int, width_depth_height: int) -> int:
        return FUNCTION_GAME_CONTROLLER_CREATE_VOXEL_POINT_LIST_WITH_WORLD_SPHERE_FOR_REMOVE(self.address, pv3_out_point_list, dw_max_buffer_count, p_bs, p_clip_plane, width_depth_height)
    
    def get_footrest_base_obj_pos(self, piv_out_obj_pos: int, pv3_pos: int, f_adj_height: float) -> bool:
        return FUNCTION_GAME_CONTROLLER_GET_FOOTREST_BASE_OBJ_POS(self.address, piv_out_obj_pos, pv3_pos, f_adj_height)
    
    def get_footrest_quad_list(self, p_out_quad_list: int, dw_max_quad_count: int, piv_base_obj_pos: int, i_tex_repeat: int, pb_out_insuffcient: int) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_FOOTREST_QUAD_LIST(self.address, p_out_quad_list, dw_max_quad_count, piv_base_obj_pos, i_tex_repeat, pb_out_insuffcient)
    
    def get_footrest_height(self, piv_base_obj_pos: int) -> float:
        return FUNCTION_GAME_CONTROLLER_GET_FOOTREST_HEIGHT(self.address, piv_base_obj_pos)
    
    def set_selected_voxel(self, p_voxel_obj_lite: int, x: int, y: int, z: int) -> None:
        FUNCTION_GAME_CONTROLLER_SET_SELECTED_VOXEL(self.address, p_voxel_obj_lite, x, y, z)
    
    def set_selected(self, p_voxel_obj_lite: int) -> None:
        FUNCTION_GAME_CONTROLLER_SET_SELECTED(self.address, p_voxel_obj_lite)
    
    def clear_selected_voxel(self, p_voxel_obj_lite: int, x: int, y: int, z: int) -> None:
        FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_VOXEL(self.address, p_voxel_obj_lite, x, y, z)
    
    def clear_selected_all(self) -> None:
        FUNCTION_GAME_CONTROLLER_CLEAR_SELECTED_ALL(self.address)
    
    def write_file(self, wch_file_name: str) -> bool:
        return FUNCTION_GAME_CONTROLLER_WRITE_FILE(self.address, wch_file_name)
    
    def read_file(self, wch_file_name: str, b_delayed_update: bool, b_lighting: bool) -> bool:
        return FUNCTION_GAME_CONTROLLER_READ_FILE(self.address, wch_file_name, b_delayed_update, b_lighting)
    
    def get_current_color_index(self) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_CURRENT_COLOR_INDEX(self.address)
    
    def get_current_edit_mode(self) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_CURRENT_EDIT_MODE(self.address)
    
    def get_current_plane_type(self) -> int:
        return FUNCTION_GAME_CONTROLLER_GET_CURRENT_PLANE_TYPE(self.address)
    
    def get_selected_voxel_obj_desc(self, p_out_voxel_obj_desc: int) -> bool:
        return FUNCTION_GAME_CONTROLLER_GET_SELECTED_VOXEL_OBJ_DESC(self.address, p_out_voxel_obj_desc)
    
    def get_cursor_status(self, pv3_out_cursor_obj_pos: int, piv_out_cursor_voxel_pos: int, pui_out_width_depth_height: int, pf_out_cursor_voxel_size: int, pb_out_color_index: int) -> bool:
        return FUNCTION_GAME_CONTROLLER_GET_CURSOR_STATUS(self.address, pv3_out_cursor_obj_pos, piv_out_cursor_voxel_pos, pui_out_width_depth_height, pf_out_cursor_voxel_size, pb_out_color_index)
    
    def is_updating(self) -> bool:
        return FUNCTION_GAME_CONTROLLER_IS_UPDATING(self.address)
    
    def update_visibility_all(self) -> None:
        FUNCTION_GAME_CONTROLLER_UPDATE_VISIBILITY_ALL(self.address)
    
    def enable_destroyable_all(self, b_switch: bool) -> None:
        FUNCTION_GAME_CONTROLLER_ENABLE_DESTROYABLE_ALL(self.address, b_switch)
    
    def enable_auto_restore_all(self, b_switch: bool) -> None:
        FUNCTION_GAME_CONTROLLER_ENABLE_AUTO_RESTORE_ALL(self.address, b_switch)
    
