import ctypes
import ctypes.wintypes as wintypes

IS_FUNCTIONS_LOADED = False

FUNCTION_NETWORK_LAYER_SEND__MIDI_NOTE_BLOCK = None
FUNCTION_NETWORK_LAYER_SEND__BEGIN_MIDI_NOTE_BLOCK = None
FUNCTION_NETWORK_LAYER_SEND__END_MIDI_NOTE_BLOCK = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_MULTIPLE_VOXELS = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_MULTIPLE_VOXELS_COLOR = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_MULTIPLE_VOXELS = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_CREATE_VOXEL_OBJECT = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_VOXEL = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_VOXEL = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_VOXEL_COLOR = None
FUNCTION_NETWORK_LAYER_SEND__REQUEST_RESIZE_VOXEL_DETAIL = None

def load_functions_of_network_layer(function_table_address: int):
    global IS_FUNCTIONS_LOADED
    
    if IS_FUNCTIONS_LOADED:
        return
    
    function_address = ctypes.cast(function_table_address + 0, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__MIDI_NOTE_BLOCK
    FUNCTION_NETWORK_LAYER_SEND__MIDI_NOTE_BLOCK = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD)(function_address)
    
    function_address = ctypes.cast(function_table_address + 8, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__BEGIN_MIDI_NOTE_BLOCK
    FUNCTION_NETWORK_LAYER_SEND__BEGIN_MIDI_NOTE_BLOCK = ctypes.CFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 16, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__END_MIDI_NOTE_BLOCK
    FUNCTION_NETWORK_LAYER_SEND__END_MIDI_NOTE_BLOCK = ctypes.CFUNCTYPE(None, wintypes.LPVOID)(function_address)
    
    function_address = ctypes.cast(function_table_address + 24, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_MULTIPLE_VOXELS
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_MULTIPLE_VOXELS = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.BYTE, wintypes.BYTE, ctypes.c_int, wintypes.BOOL)(function_address)
    
    function_address = ctypes.cast(function_table_address + 32, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_MULTIPLE_VOXELS_COLOR
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_MULTIPLE_VOXELS_COLOR = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.BYTE, wintypes.BYTE, ctypes.c_int)(function_address)
    
    function_address = ctypes.cast(function_table_address + 40, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_MULTIPLE_VOXELS
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_MULTIPLE_VOXELS = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.BYTE, ctypes.c_int)(function_address)
    
    function_address = ctypes.cast(function_table_address + 48, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_CREATE_VOXEL_OBJECT
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_CREATE_VOXEL_OBJECT = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT, ctypes.c_float, wintypes.WORD, wintypes.BYTE, wintypes.BOOL)(function_address)
    
    function_address = ctypes.cast(function_table_address + 56, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_VOXEL
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_VOXEL = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE, wintypes.BYTE, wintypes.BOOL)(function_address)
    
    function_address = ctypes.cast(function_table_address + 64, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_VOXEL
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_VOXEL = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 72, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_VOXEL_COLOR
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_VOXEL_COLOR = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE, wintypes.BYTE)(function_address)
    
    function_address = ctypes.cast(function_table_address + 80, ctypes.POINTER(ctypes.c_void_p))[0]
    global FUNCTION_NETWORK_LAYER_SEND__REQUEST_RESIZE_VOXEL_DETAIL
    FUNCTION_NETWORK_LAYER_SEND__REQUEST_RESIZE_VOXEL_DETAIL = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE)(function_address)
        
    IS_FUNCTIONS_LOADED = True

class NetworkLayer:
    address: int = None
    
    def __init__(self, address: int):
        self.address = address
        
        function_table_address = ctypes.cast(address, ctypes.POINTER(ctypes.c_void_p))[0]
        load_functions_of_network_layer(function_table_address)
    
    def send__midi_note_block(self, p_note_list: int, dw_note_num: int) -> None:
        FUNCTION_NETWORK_LAYER_SEND__MIDI_NOTE_BLOCK(self.address, p_note_list, dw_note_num)
    
    def send__begin_midi_note_block(self) -> None:
        FUNCTION_NETWORK_LAYER_SEND__BEGIN_MIDI_NOTE_BLOCK(self.address)
    
    def send__end_midi_note_block(self) -> None:
        FUNCTION_NETWORK_LAYER_SEND__END_MIDI_NOTE_BLOCK(self.address)
    
    def send__request_add_multiple_voxels(self, pv3_obj_pos: int, piv_voxel_pos_list: int, dw_voxel_num: int, b_width_depth_height: int, b_color_index: int, plane_type: int, b_rebuild_area: bool) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_MULTIPLE_VOXELS(self.address, pv3_obj_pos, piv_voxel_pos_list, dw_voxel_num, b_width_depth_height, b_color_index, plane_type, b_rebuild_area)
    
    def send__request_set_multiple_voxels_color(self, pv3_obj_pos: int, piv_voxel_pos_list: int, dw_voxel_num: int, b_color_index: int, width_depth_height: int, plane_type: int) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_MULTIPLE_VOXELS_COLOR(self.address, pv3_obj_pos, piv_voxel_pos_list, dw_voxel_num, b_color_index, width_depth_height, plane_type)
    
    def send__request_remove_multiple_voxels(self, pv3_obj_pos: int, piv_voxel_pos_list: int, dw_voxel_num: int, b_width_depth_height: int, plane_type: int) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_MULTIPLE_VOXELS(self.address, pv3_obj_pos, piv_voxel_pos_list, dw_voxel_num, b_width_depth_height, plane_type)
    
    def send__request_create_voxel_object(self, pv3_obj_pos: int, width_depth_height: int, f_voxel_size: float, w_first_voxel_pos: int, b_first_voxel_color: int, b_rebuild_area: bool) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_CREATE_VOXEL_OBJECT(self.address, pv3_obj_pos, width_depth_height, f_voxel_size, w_first_voxel_pos, b_first_voxel_color, b_rebuild_area)
    
    def send__request_add_voxel(self, pv3_obj_pos: int, p_voxel_pos: int, b_width_depth_height: int, b_voxel_color: int, b_rebuild_area: bool) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_ADD_VOXEL(self.address, pv3_obj_pos, p_voxel_pos, b_width_depth_height, b_voxel_color, b_rebuild_area)
    
    def send__request_remove_voxel(self, pv3_obj_pos: int, p_voxel_pos: int, b_width_depth_height: int) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_REMOVE_VOXEL(self.address, pv3_obj_pos, p_voxel_pos, b_width_depth_height)
    
    def send__request_set_voxel_color(self, pv3_obj_pos: int, p_voxel_pos: int, b_color_index: int, width_depth_height: int) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_SET_VOXEL_COLOR(self.address, pv3_obj_pos, p_voxel_pos, b_color_index, width_depth_height)
    
    def send__request_resize_voxel_detail(self, pv3_obj_pos: int, width_depth_height: int) -> None:
        FUNCTION_NETWORK_LAYER_SEND__REQUEST_RESIZE_VOXEL_DETAIL(self.address, pv3_obj_pos, width_depth_height)
    
