import ctypes
import os
import psutil
from ctypes import wintypes

class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [('nLength', wintypes.DWORD),
                ('lpSecurityDescriptor', wintypes.LPVOID),
                ('bInheritHandle', wintypes.BOOL), ]


DLL_INJECTOR_LPSECURITY_ATTRIBUTES                  = ctypes.POINTER(_SECURITY_ATTRIBUTES)
DLL_INJECTOR_PAGE_READWRITE                         = 0x04
DLL_INJECTOR_PROCESS_ALL_ACCESS                     = (0x00F0000 | 0x00100000 | 0xFFF)
DLL_INJECTOR_VIRTUAL_MEMORY                         = (0x1000 | 0x2000)
DLL_INJECTOR_DEALLOCATE_MEMORY                      = 0x8000

DLL_INJECTOR_KERNEL32                               = ctypes.WinDLL('kernel32', use_last_error=True)
DLL_INJECTOR_PSAPI                                  = ctypes.windll.psapi

DLL_INJECTOR_KERNEL32.OpenProcess.restype           = wintypes.HANDLE
DLL_INJECTOR_KERNEL32.OpenProcess.argtypes          = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]

DLL_INJECTOR_KERNEL32.CloseHandle.restype           = wintypes.BOOL
DLL_INJECTOR_KERNEL32.CloseHandle.argtypes          = [wintypes.HANDLE]

DLL_INJECTOR_KERNEL32.LoadLibraryA.restype          = wintypes.HANDLE
DLL_INJECTOR_KERNEL32.LoadLibraryA.argtypes         = [wintypes.LPCSTR]

DLL_INJECTOR_KERNEL32.GetModuleHandleW.restype      = wintypes.HMODULE
DLL_INJECTOR_KERNEL32.GetModuleHandleW.argtypes     = [wintypes.LPCWSTR]

DLL_INJECTOR_KERNEL32.GetProcAddress.restype        = wintypes.LPVOID
DLL_INJECTOR_KERNEL32.GetProcAddress.argtypes       = [wintypes.HANDLE, wintypes.LPCSTR]

DLL_INJECTOR_KERNEL32.VirtualAllocEx.restype        = wintypes.LPVOID
DLL_INJECTOR_KERNEL32.VirtualAllocEx.argtypes       = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD, wintypes.DWORD]

DLL_INJECTOR_KERNEL32.VirtualFreeEx.restype         = wintypes.BOOL
DLL_INJECTOR_KERNEL32.VirtualFreeEx.argtypes        = [wintypes.HANDLE, wintypes.LPVOID, ctypes.c_size_t, wintypes.DWORD]

DLL_INJECTOR_KERNEL32.WriteProcessMemory.restype    = wintypes.BOOL
DLL_INJECTOR_KERNEL32.WriteProcessMemory.argtypes   = [wintypes.HANDLE, wintypes.LPVOID, wintypes.LPCVOID, wintypes.DWORD, ctypes.POINTER(ctypes.c_int)]

DLL_INJECTOR_KERNEL32.CreateRemoteThread.restype    = wintypes.HANDLE
DLL_INJECTOR_KERNEL32.CreateRemoteThread.argtypes   = [wintypes.HANDLE, DLL_INJECTOR_LPSECURITY_ATTRIBUTES, ctypes.c_size_t, wintypes.LPVOID, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD]

DLL_INJECTOR_KERNEL32.WaitForSingleObject.restype   = wintypes.DWORD
DLL_INJECTOR_KERNEL32.WaitForSingleObject.argtypes  = [wintypes.HANDLE, wintypes.DWORD]

DLL_INJECTOR_KERNEL32.GetExitCodeThread.restype     = wintypes.BOOL
DLL_INJECTOR_KERNEL32.GetExitCodeThread.argtypes    = [wintypes.HANDLE, wintypes.LPDWORD]

DLL_INJECTOR_PSAPI.GetModuleFileNameExW.restype     = wintypes.DWORD
DLL_INJECTOR_PSAPI.GetModuleFileNameExW.argtypes    = [wintypes.HANDLE, wintypes.HMODULE, wintypes.LPWSTR, wintypes.DWORD]

DLL_INJECTOR_PSAPI.EnumProcessModules.restype       = wintypes.BOOL
DLL_INJECTOR_PSAPI.EnumProcessModules.argtypes      = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD, wintypes.LPDWORD]

DLL_INJECTOR_LOAD_LIBRARY_W_ADDRESS = None

DLL_INJECTOR_KERNEL32_HANDLE = DLL_INJECTOR_KERNEL32.GetModuleHandleW('kernel32.dll')

if not DLL_INJECTOR_KERNEL32_HANDLE:
    error = ctypes.get_last_error()
    raise Exception("Failed to get kernel32 handle. %d - %s" % (error, ctypes.FormatError(error)))

DLL_INJECTOR_LOAD_LIBRARY_W_ADDRESS = DLL_INJECTOR_KERNEL32.GetProcAddress(DLL_INJECTOR_KERNEL32_HANDLE, b"LoadLibraryW")

if not DLL_INJECTOR_LOAD_LIBRARY_W_ADDRESS:
    error = ctypes.get_last_error()
    raise Exception("Failed to get 'LoadLibraryW' address. %d - %s" % (error, ctypes.FormatError(error)))

def get_function_address_with_module_path(module_path, function_name):
    base_address = DLL_INJECTOR_KERNEL32.LoadLibraryA(module_path.encode("ascii"))
    
    function_address = DLL_INJECTOR_KERNEL32.GetProcAddress(base_address, function_name.encode("ascii"))

    if not function_address:
        error = ctypes.get_last_error()
        raise Exception("Failed to call 'GetProcAddress' function. %d - %s" % (error, ctypes.FormatError(error)))

    return function_address - base_address

def get_function_address_with_module_address(module_address, function_name):
    function_address = DLL_INJECTOR_KERNEL32.GetProcAddress(module_address, function_name.encode("ascii"))

    if not function_address:
        error = ctypes.get_last_error()
        raise Exception("Failed to call 'GetProcAddress' function. %d - %s" % (error, ctypes.FormatError(error)))

    return function_address - module_address
    
class DLLInjector:
    def __init__(self):
        self.process_handle = None
        self.memories = []
        
    def bind_by_name(self, process_name):
        target_pid = None
        
        for process in psutil.process_iter(['name', 'pid']):
            if process.info['name'] == process_name:
                target_pid = process.info['pid']
                break
        
        if not target_pid:
            raise Exception("Failed to find a process named '%s'." % (process_name))

        self.bind(target_pid)
        
    def bind(self, process_pid):
        if self.process_handle:
            raise Exception("Failed to bind porcess because the process already binded.")
        
        self.process_handle = DLL_INJECTOR_KERNEL32.OpenProcess(DLL_INJECTOR_PROCESS_ALL_ACCESS, False, int(process_pid))

        if not self.process_handle:
            error = ctypes.get_last_error()
            raise Exception("Failed to call 'OpenProcess' function. %d - %s" % (error, ctypes.FormatError(error)))
    
    def unbind(self):
        if not self.process_handle:
            raise Exception("Failed to unbind process the process was not binded.")
        
        DLL_INJECTOR_KERNEL32.CloseHandle(self.process_handle)
        
        for address in self.memories:
            self.deallocate(address)

        self.process_handle = None

    def allocate(self, size):
        if not self.process_handle:
            raise Exception("Failed to allocate because the process was not binded.")
        
        address = DLL_INJECTOR_KERNEL32.VirtualAllocEx(self.process_handle, 0, size, DLL_INJECTOR_VIRTUAL_MEMORY, DLL_INJECTOR_PAGE_READWRITE)
        
        if address <= 0:
            error = ctypes.get_last_error()
            raise Exception("Failed to call 'VirtualAllocEx' function. %d - %s" % (error, ctypes.FormatError(error)))
    
        self.memories.append(address)

        return address
    
    def deallocate(self, address):
        if not self.process_handle:
            raise Exception("Failed to deallocate because the process was not binded.")
        
        if not DLL_INJECTOR_KERNEL32.VirtualFreeEx (self.process_handle, address, 0, DLL_INJECTOR_DEALLOCATE_MEMORY):
            error = ctypes.get_last_error()
            raise Exception("Failed to call 'VirtualFreeEx' function. %d - %s" % (error, ctypes.FormatError(error)))
    
        self.memories.remove(address)
    
    def write(self, address, data, length):
        if not self.process_handle:
            raise Exception("Failed to write memory because the process was not binded.")
        
        written_bytes = ctypes.c_int(0)
        write_status = DLL_INJECTOR_KERNEL32.WriteProcessMemory(self.process_handle, address, data, length, ctypes.byref(written_bytes))

        if written_bytes.value != length:
            raise Exception("Failed to write all bytes to memory.")

        if not write_status:
            error = ctypes.get_last_error()
            raise Exception("Failed to write bytes to memory. %d - %s" % (error, ctypes.FormatError(error)))
    
    def write_wide_characters(self, address, string):
        if not self.process_handle:
            raise Exception("Failed to write memory because the process was not binded.")
        
        self.write(address, string.encode('utf-16-le') + b'\0\0', (len(string) + 1) * 2)
    
    def create_remote_thread(self, function_address, argument_address):
        if not self.process_handle:
            raise Exception("Failed to write memory because the process was not binded.")
        
        thread_id = ctypes.c_ulong(0)    
        thread_handle = DLL_INJECTOR_KERNEL32.CreateRemoteThread(self.process_handle, None, 0, function_address, argument_address, 0, ctypes.byref(thread_id))
        
        if not thread_handle:
            error = ctypes.get_last_error()
            raise Exception("Failed to create remote thread. %d - %s" % (error, ctypes.FormatError(error)))

        if DLL_INJECTOR_KERNEL32.WaitForSingleObject(thread_handle, 0xFFFFFFFF) == 0xFFFFFFFF:
            error = ctypes.get_last_error()
            raise Exception("Failed to wait for thread execute done. %d - %s" % (error, ctypes.FormatError(error)))
        
    def call(self, module_address, function_address, argument_address):
        if not self.process_handle:
            raise Exception("Failed to call function because the process was not binded.")
    
        thread_id = ctypes.c_ulong(0)    
        thread_handle = DLL_INJECTOR_KERNEL32.CreateRemoteThread(self.process_handle, None, 0, module_address + function_address, argument_address, 0, ctypes.byref(thread_id))
        
        if not thread_handle:
            error = ctypes.get_last_error()
            raise Exception("Failed to call function because fail create remote thread. %d - %s" % (error, ctypes.FormatError(error)))

        if DLL_INJECTOR_KERNEL32.WaitForSingleObject(thread_handle, 0xFFFFFFFF) == 0xFFFFFFFF:
            error = ctypes.get_last_error()
            raise Exception("Failed to call function because fail 'WaitForSingleObject'. %d - %s" % (error, ctypes.FormatError(error)))
    
    def get_module_list(self):
        storedBytes = wintypes.DWORD()
        
        if not DLL_INJECTOR_PSAPI.EnumProcessModules(self.process_handle, 0, 0, ctypes.byref(storedBytes)):
            error = ctypes.get_last_error()
            raise Exception("Failed to get module list because fail 'EnumProcessModules'. %d - %s" % (error, ctypes.FormatError(error)))
        
        needLength = storedBytes.value // ctypes.sizeof(wintypes.HMODULE)
        moduleHandles = (wintypes.HMODULE * needLength)()
        
        if not DLL_INJECTOR_PSAPI.EnumProcessModules(self.process_handle, ctypes.byref(moduleHandles), int(ctypes.sizeof(wintypes.HMODULE) * needLength), ctypes.byref(storedBytes)):
            error = ctypes.get_last_error()
            raise Exception("Failed to get module list because fail 'EnumProcessModules'. %d - %s" % (error, ctypes.FormatError(error)))
        
        moduleNameBuffer = ctypes.create_unicode_buffer(wintypes.MAX_PATH)
        results = []

        for index in range(0, needLength):
            if moduleHandles[index]:
                if not DLL_INJECTOR_PSAPI.GetModuleFileNameExW(self.process_handle, moduleHandles[index], moduleNameBuffer, wintypes.MAX_PATH):
                    error = ctypes.get_last_error()
                    raise Exception("Failed to get module list because fail 'GetModuleFileNameW'. %d - %s" % (error, ctypes.FormatError(error)))
                
                results.append({
                    'name': moduleNameBuffer.value,
                    'handle': moduleHandles[index]
                })

        return results

    def load_module(self, module_path):
        if not self.process_handle:
            raise Exception("Failed to load module because the process was not binded.")
        
        module_path = os.path.abspath(module_path)
        module_path_address = self.allocate((len(module_path) + 1) * 2)

        try:
            self.write_wide_characters(module_path_address, module_path)
        
            self.create_remote_thread(DLL_INJECTOR_LOAD_LIBRARY_W_ADDRESS, module_path_address)
            
            loaded_modules = self.get_module_list()

            for module in loaded_modules:
                if module_path.casefold() == os.path.abspath(module['name']).casefold():
                    return module['handle']

            raise Exception("Failed to load module because not found module handle in process.")
        finally:
            self.deallocate(module_path_address)