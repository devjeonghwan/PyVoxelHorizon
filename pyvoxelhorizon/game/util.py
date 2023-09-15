import ctypes

def read_pointer_chain(address: int, offsets: list[int]):
    for offset in offsets:
        address = ctypes.cast(address + offset, ctypes.POINTER(ctypes.c_void_p))[0]

    return address

def read_memory(address: int, type: int):
    return ctypes.cast(address, ctypes.POINTER(type))[0]