import ctypes

def get_address(object):
    if isinstance(object, AddressObject):
        return object.address
    
    return ctypes.addressof(object)

def cast_address(address: int, type: type):
    if issubclass(type, AddressObject):
        return type(address)
    
    return ctypes.cast(address, ctypes.POINTER(type)).contents

class AddressObject:
    address: int = None
    
    def __init__(self, address: int):
        self.address = address
