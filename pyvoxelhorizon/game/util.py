import ctypes

def read_pointer_chain(address, offsets):
    for offset in offsets:
        address = ctypes.cast(address + offset, ctypes.POINTER(ctypes.c_void_p))[0]

    return address

def read_memory(address, type):
    return ctypes.cast(address, ctypes.POINTER(type))[0]