import ctypes


def get_addresses_pointer(objects: list[object]) -> int:
    pointer_array = (ctypes.c_ulong * len(objects))()

    for index in range(len(objects)):
        pointer_array[index] = get_address(objects[index])

    return get_address(pointer_array)


def get_address(object) -> int:
    if isinstance(object, AddressObject):
        return object.address

    return ctypes.addressof(object)


def cast_address(address: int, type: type):
    if not address:
        return None

    if issubclass(type, AddressObject):
        return type(address)

    return ctypes.cast(address, ctypes.POINTER(type)).contents


class AddressObject:
    address: int = None

    def __init__(self, address: int):
        self.address = address
