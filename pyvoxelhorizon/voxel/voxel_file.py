import struct

from .voxel_object import VoxelObject
from .constant import *

class VoxelFile:
    # struct VOXELS_FILE_HEADER
    # {
    # 	DWORD	dwVersion;
    # 	DWORD	dwVoxelObjNum;
    # 	DWORD	dwLightNum;
    # 	float	fWhitePoint;
    # 	DWORD	dwReserved[15];
    # 	DWORD	dwStreamSize;
    # };
    def __init__(self):
        self.white_point = float()
        # Make linear data structure to hash data structure for optimization.
        self.object_map = {}

    def __getitem__(self, position):
        x, y, z = position

        object = self.get_object(x, y, z)

        if object != None:
            return object

        return self.create_object(x, y, z)

    def get_objects(self):
        objects = []

        for k, x_map in self.object_map.items():
            for k, y_map in x_map.items():
                for k, object in y_map.items():
                    objects.append(object)

        return objects

    def get_object(self, x, y, z):
        map = self.object_map

        if x not in map:
            return None
        map = map[x]

        if y not in map:
            return None
        map = map[y]

        if z not in map:
            return None

        return map[z]

    def append_object(self, object):
        x = object.position.x
        y = object.position.y
        z = object.position.z

        if self.get_object(x, y, z) != None:
            raise ValueError(
                "Already exists object of {0}, {1}, {2}.", x, y, z)

        map = self.object_map

        if x not in map:
            map[x] = {}
        map = map[x]

        if y not in map:
            map[y] = {}
        map = map[y]

        map[z] = object

        return object

    def create_object(self, x, y, z):
        object = VoxelObject()

        object.position.x = x
        object.position.y = y
        object.position.z = z

        return self.append_object(object)

    def to_bytes(self, compress=False):
        dirty_objects = self.get_objects()
        objects = [object for object in dirty_objects if not object.is_empty()]

        data = bytes()

        # Write Version
        data += int.to_bytes(VH_VOXEL_FILE_VERSION, 4, 'little', signed=False)

        # Write Object Count
        data += int.to_bytes(len(objects), 4, 'little', signed=False)

        # Write Light Count
        data += int.to_bytes(0, 4, 'little', signed=False)

        # Write White Point
        data += struct.pack('f', self.white_point)

        # Write Reserved
        data += bytes(4 * 15)

        stream_data = bytes()
        for object in objects:
            object_data = object.to_bytes(compress)

            # Write Object Size
            stream_data += int.to_bytes(len(object_data),
                                        4, 'little', signed=False)

            # Write Object Data
            stream_data += object_data

        # Write Stream Size
        data += int.to_bytes(len(stream_data), 4, 'little', signed=False)

        # Write Stream Data
        data += stream_data

        return data

    @staticmethod
    def from_file(path):
        file_descriptor = open(path, 'rb')
        data = file_descriptor.read()
        file_descriptor.close()

        return VoxelFile.from_bytes(data)

    @staticmethod
    def from_bytes(bytes, offset=0):
        if len(bytes) < 80:
            raise ValueError("Voxel file size must be greater than 80 bytes.")

        instance = VoxelFile()

        # Read Version
        version = int.from_bytes(bytes[0:4], 'little', signed=False)
        offset += 4

        if version != VH_VOXEL_FILE_VERSION:
            raise ValueError(
                "The currently supported file version is {0}.".format(VH_VOXEL_FILE_VERSION))

        # Read Object Count
        voxel_object_count = int.from_bytes(bytes[4:8], 'little', signed=False)
        offset += 4

        # Read Light Count
        light_count = int.from_bytes(bytes[8:12], 'little', signed=False)
        offset += 4

        # Read White Point
        instance.white_point = struct.unpack('f', bytes[12:16])[0]
        offset += 4

        # Skip Reserved
        offset += 60

        # Read Stream Size
        stream_size = int.from_bytes(bytes[76:80], 'little', signed=False)
        offset += 4

        for i in range(voxel_object_count):
            # Read Object Size
            object_size = int.from_bytes(
                bytes[offset + 0:offset + 4], 'little', signed=False)
            offset += 4

            # Read Object Data
            object = VoxelObject.from_bytes(bytes, offset)

            instance.append_object(object)
            offset += object_size

        return instance