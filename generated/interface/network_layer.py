import ctypes
import ctypes.wintypes as wintypes

from pyvoxelhorizon.util import *
from pyvoxelhorizon.enum import *
from pyvoxelhorizon.struct.vector3 import Vector3
from pyvoxelhorizon.struct.int_vector3 import IntVector3

IS_FUNCTIONS_LOADED = False

FUNCTION_NETWORK_LAYER_SEND_REQUESTADDMULTIPLEVOXELS = None
FUNCTION_NETWORK_LAYER_SEND_REQUESTSETMULTIPLEVOXELSCOLOR = None
FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEMULTIPLEVOXELS = None
FUNCTION_NETWORK_LAYER_SEND_REQUESTCREATEVOXELOBJECT = None
FUNCTION_NETWORK_LAYER_SEND_REQUESTADDVOXEL = None
FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEVOXEL = None
FUNCTION_NETWORK_LAYER_SEND_REQUESTSETVOXELCOLOR = None
FUNCTION_NETWORK_LAYER_SEND_REQUESTRESIZEVOXELDETAIL = None


def load_functions_of_network_layer(function_table_address: int):
    global IS_FUNCTIONS_LOADED
    
    if IS_FUNCTIONS_LOADED:
        return
    
    function_address = read_memory(function_table_address + 0, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTADDMULTIPLEVOXELS
    FUNCTION_NETWORK_LAYER_SEND_REQUESTADDMULTIPLEVOXELS = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.BYTE, wintypes.BYTE, ctypes.c_int, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 8, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTSETMULTIPLEVOXELSCOLOR
    FUNCTION_NETWORK_LAYER_SEND_REQUESTSETMULTIPLEVOXELSCOLOR = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.BYTE, wintypes.BYTE, ctypes.c_int)(function_address)
    
    function_address = read_memory(function_table_address + 16, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEMULTIPLEVOXELS
    FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEMULTIPLEVOXELS = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.BYTE, ctypes.c_int)(function_address)
    
    function_address = read_memory(function_table_address + 24, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTCREATEVOXELOBJECT
    FUNCTION_NETWORK_LAYER_SEND_REQUESTCREATEVOXELOBJECT = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.UINT, ctypes.c_float, wintypes.WORD, wintypes.BYTE, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 32, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTADDVOXEL
    FUNCTION_NETWORK_LAYER_SEND_REQUESTADDVOXEL = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE, wintypes.BYTE, wintypes.BOOL)(function_address)
    
    function_address = read_memory(function_table_address + 40, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEVOXEL
    FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEVOXEL = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE)(function_address)
    
    function_address = read_memory(function_table_address + 48, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTSETVOXELCOLOR
    FUNCTION_NETWORK_LAYER_SEND_REQUESTSETVOXELCOLOR = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE, wintypes.BYTE)(function_address)
    
    function_address = read_memory(function_table_address + 56, ctypes.c_void_p)
    global FUNCTION_NETWORK_LAYER_SEND_REQUESTRESIZEVOXELDETAIL
    FUNCTION_NETWORK_LAYER_SEND_REQUESTRESIZEVOXELDETAIL = ctypes.CFUNCTYPE(None, wintypes.LPVOID, wintypes.LPVOID, wintypes.BYTE)(function_address)
        
    IS_FUNCTIONS_LOADED = True


class NetworkLayer(AddressObject):
    def __init__(self, address: int):
        super().__init__(address)
        
        function_table_address = read_memory(address, ctypes.c_void_p)
        load_functions_of_network_layer(function_table_address)
    
    def send_requestaddmultiplevoxels(self, pv3_obj_pos: Vector3, piv_voxel_pos_list: IntVector3, dw_voxel_num: int, b_width_depth_height: int, b_color_index: int, plane_type: int, b_rebuild_area: bool) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        piv_voxel_pos_list = get_address(piv_voxel_pos_list)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTADDMULTIPLEVOXELS(self.address, pv3_obj_pos, piv_voxel_pos_list, dw_voxel_num, b_width_depth_height, b_color_index, plane_type, b_rebuild_area)
    
    def send_requestsetmultiplevoxelscolor(self, pv3_obj_pos: Vector3, piv_voxel_pos_list: IntVector3, dw_voxel_num: int, b_color_index: int, width_depth_height: int, plane_type: int) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        piv_voxel_pos_list = get_address(piv_voxel_pos_list)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTSETMULTIPLEVOXELSCOLOR(self.address, pv3_obj_pos, piv_voxel_pos_list, dw_voxel_num, b_color_index, width_depth_height, plane_type)
    
    def send_requestremovemultiplevoxels(self, pv3_obj_pos: Vector3, piv_voxel_pos_list: IntVector3, dw_voxel_num: int, b_width_depth_height: int, plane_type: int) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        piv_voxel_pos_list = get_address(piv_voxel_pos_list)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEMULTIPLEVOXELS(self.address, pv3_obj_pos, piv_voxel_pos_list, dw_voxel_num, b_width_depth_height, plane_type)
    
    def send_requestcreatevoxelobject(self, pv3_obj_pos: Vector3, width_depth_height: int, f_voxel_size: float, w_first_voxel_pos: int, b_first_voxel_color: int, b_rebuild_area: bool) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTCREATEVOXELOBJECT(self.address, pv3_obj_pos, width_depth_height, f_voxel_size, w_first_voxel_pos, b_first_voxel_color, b_rebuild_area)
    
    def send_requestaddvoxel(self, pv3_obj_pos: Vector3, p_voxel_pos: IntVector3, b_width_depth_height: int, b_voxel_color: int, b_rebuild_area: bool) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        p_voxel_pos = get_address(p_voxel_pos)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTADDVOXEL(self.address, pv3_obj_pos, p_voxel_pos, b_width_depth_height, b_voxel_color, b_rebuild_area)
    
    def send_requestremovevoxel(self, pv3_obj_pos: Vector3, p_voxel_pos: IntVector3, b_width_depth_height: int) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        p_voxel_pos = get_address(p_voxel_pos)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTREMOVEVOXEL(self.address, pv3_obj_pos, p_voxel_pos, b_width_depth_height)
    
    def send_requestsetvoxelcolor(self, pv3_obj_pos: Vector3, p_voxel_pos: IntVector3, b_color_index: int, width_depth_height: int) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        p_voxel_pos = get_address(p_voxel_pos)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTSETVOXELCOLOR(self.address, pv3_obj_pos, p_voxel_pos, b_color_index, width_depth_height)
    
    def send_requestresizevoxeldetail(self, pv3_obj_pos: Vector3, width_depth_height: int) -> None:
        pv3_obj_pos = get_address(pv3_obj_pos)
        
        return FUNCTION_NETWORK_LAYER_SEND_REQUESTRESIZEVOXELDETAIL(self.address, pv3_obj_pos, width_depth_height)
    
