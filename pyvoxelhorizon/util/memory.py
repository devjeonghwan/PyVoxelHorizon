import ctypes

def read_memory(address: int, type: type):
    return ctypes.cast(address, ctypes.POINTER(type))[0]