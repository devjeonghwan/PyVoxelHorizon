import struct
import math
from threading import local

VH_WIDTH_DEPTH_HEIGHT_2BITS = 0b11
VH_PROPERTY_2BITS = 0b1100
VH_PROPERTY_DESTROYABLE_1BITS = 0b0100
VH_PROPERTY_RESERVED_1BITS = 0b1000
VH_COLOR_TABLE_SIZE_10BITS = 0b1111111111
VH_COLOR_TABLE_SIZE_MASK = VH_COLOR_TABLE_SIZE_10BITS << 4
VH_COLOR_TABLE_COMPRESSED_MASK = 0b1 << 14
VH_GEOMETRY_COMPRESSED_MASK = 0b1 << 15

VH_VOXEL_FILE_VERSION = 7
VH_MAX_WIDTH_DEPTH_HEIGHT = 8
VH_DEFAULT_WIDTH_DEPTH_HEIGHT = 8


class Color:
    def __init__(self, rgb=(0, 0, 0)):
        self.red = rgb[0]
        self.green = rgb[1]
        self.blue = rgb[2]


VH_COLORS = [
    Color(rgb=(71, 45, 60)),
    Color(rgb=(94, 54, 67)),
    Color(rgb=(122, 68, 74)),
    Color(rgb=(160, 91, 83)),
    Color(rgb=(191, 121, 88)),
    Color(rgb=(238, 161, 96)),
    Color(rgb=(244, 204, 161)),
    Color(rgb=(182, 213, 60)),
    Color(rgb=(113, 170, 52)),
    Color(rgb=(57, 123, 68)),
    Color(rgb=(60, 89, 86)),
    Color(rgb=(48, 44, 46)),
    Color(rgb=(90, 83, 83)),
    Color(rgb=(125, 112, 113)),
    Color(rgb=(160, 147, 142)),
    Color(rgb=(207, 198, 184)),

    Color(rgb=(223, 246, 245)),
    Color(rgb=(138, 235, 241)),
    Color(rgb=(40, 204, 223)),
    Color(rgb=(57, 120, 168)),
    Color(rgb=(57, 71, 120)),
    Color(rgb=(57, 49, 75)),
    Color(rgb=(86, 64, 100)),
    Color(rgb=(142, 71, 140)),
    Color(rgb=(205, 96, 147)),
    Color(rgb=(255, 174, 182)),
    Color(rgb=(244, 180, 27)),
    Color(rgb=(244, 126, 27)),
    Color(rgb=(230, 72, 46)),
    Color(rgb=(169, 59, 59)),
    Color(rgb=(130, 112, 148)),
    Color(rgb=(79, 84, 107))
]


def find_similar_color(red, green, blue):
    find_distance = 255 * 255 * 255
    find_index = None

    for index in range(len(VH_COLORS)):
        color = VH_COLORS[index]
        distance = (abs(color.red - red) + abs(color.green -
                    green) + abs(color.blue - blue)) / 3

        if find_distance > distance:
            find_distance = distance
            find_index = index

    return find_index


def get_lsb_number(n):
    count = 0

    while True:
        if n <= 1:
            return count

        n = n >> 1
        count = count + 1


class VoxelShortPosition:
    # struct VOXEL_SHORT_POS
    # {
    # 	short	x;
    # 	short	y;
    # 	short	z;
    # };
    def __init__(self):
        self.x = int()
        self.y = int()
        self.z = int()

    def to_bytes(self):
        data = bytes()

        # Write X
        data += int.to_bytes(self.x, 2, 'little', signed=True)

        # Write Y
        data += int.to_bytes(self.y, 2, 'little', signed=True)

        # Write Z
        data += int.to_bytes(self.z, 2, 'little', signed=True)

        return data

    @staticmethod
    def from_bytes(bytes, offset=0):
        if len(bytes) != 6:
            raise ValueError("ShortPosition size must be equals to 6 bytes.")

        instance = VoxelShortPosition()

        # Read X
        instance.x = int.from_bytes(
            bytes[offset:offset + 2], 'little', signed=True)
        offset += 2

        # Read Y
        instance.y = int.from_bytes(
            bytes[offset:offset + 2], 'little', signed=True)
        offset += 2

        # Read Z
        instance.z = int.from_bytes(
            bytes[offset:offset + 2], 'little', signed=True)
        offset += 2

        return instance


class VoxelWordPosition:
    # struct VOXEL_WORD_POS
    # {
    # 	WORD	x;
    # 	WORD	y;
    # 	WORD	z;
    # };
    def __init__(self):
        self.x = int()
        self.y = int()
        self.z = int()

    def to_bytes(self):
        data = bytes()

        # Write X
        data += int.to_bytes(self.x, 2, 'little', signed=False)

        # Write Y
        data += int.to_bytes(self.y, 2, 'little', signed=False)

        # Write Z
        data += int.to_bytes(self.z, 2, 'little', signed=False)

        return data

    @staticmethod
    def from_bytes(bytes, offset=0):
        if len(bytes) != 6:
            raise ValueError("WordPosition size must be equals to 6 bytes.")

        instance = VoxelWordPosition()

        # Read X
        instance.x = int.from_bytes(
            bytes[offset:offset + 2], 'little', signed=False)
        offset += 2

        # Read Y
        instance.y = int.from_bytes(
            bytes[offset:offset + 2], 'little', signed=False)
        offset += 2

        # Read Z
        instance.z = int.from_bytes(
            bytes[offset:offset + 2], 'little', signed=False)
        offset += 2

        return instance


class VoxelObject:
    # struct VOXEL_OBJECT_STREAM_COMMON_HEADER
    # {
    # 	VOXEL_SHORT_POS	Pos;
    # 	WORD	wProps;
    # }
    # struct VOXEL_OBJECT_FILE_STREAM_HEADER : VOXEL_OBJECT_STREAM_COMMON_HEADER
    # {
    # 	INT64	i64OwnerSerial;
    # 	DWORD	pData[1];
    # }
    def __init__(self, width_depth_height=VH_DEFAULT_WIDTH_DEPTH_HEIGHT, voxel_data=None, color_table=None):
        self.position = VoxelShortPosition()

        self.destroyable = False

        self.width_depth_height = None
        self.voxel_data = None
        self.color_table = None

        self.owner_serial = -1

        if voxel_data != None and color_table != None:
            self.width_depth_height = width_depth_height
            self.voxel_data = voxel_data
            self.color_table = color_table
        else:
            self.resize(width_depth_height)

    def resize(self, width_depth_height):
        if width_depth_height < 1 or width_depth_height > VH_MAX_WIDTH_DEPTH_HEIGHT:
            raise ValueError("width_depth_height must be greater than 0 and less than {0}.".format(
                VH_MAX_WIDTH_DEPTH_HEIGHT + 1))

        old_width_depth_height = self.width_depth_height
        self.width_depth_height = width_depth_height

        old_voxel_data = self.voxel_data
        old_color_table = self.color_table

        self.voxel_data = bytearray(self.get_voxel_data_size())
        self.color_table = bytearray(int(math.pow(self.width_depth_height, 3)))

        if old_voxel_data != None and old_color_table != None:
            # Rescale Data
            old_object = VoxelObject(width_depth_height=old_width_depth_height,
                                     voxel_data=old_voxel_data, color_table=old_color_table)

            ratio = old_width_depth_height / width_depth_height

            for z in range(self.width_depth_height):
                for y in range(self.width_depth_height):
                    for x in range(self.width_depth_height):
                        old_x = int(x * ratio)
                        old_y = int(y * ratio)
                        old_z = int(z * ratio)

                        self.set_voxel_raw(
                            x, y, z, old_object.get_voxel_raw(old_x, old_y, old_z))
                        self.set_voxel_color_raw(
                            x, y, z, old_object.get_voxel_color_raw(old_x, old_y, old_z))

            old_voxel_data = None
            old_color_table = None

    def get_voxel_data_size(self):
        voxel_full_count = math.pow(self.width_depth_height, 3)
        return int(voxel_full_count / 8 + (voxel_full_count % 8 != 0))

    def set_voxel(self, x, y, z, value, width_depth_height=VH_MAX_WIDTH_DEPTH_HEIGHT):
        if width_depth_height != self.width_depth_height:
            self.resize(width_depth_height)

        self.set_voxel_raw(x, y, z, value)

    def set_voxel_raw(self, x, y, z, value):
        index = int(x + (z * self.width_depth_height) +
                    (y * self.width_depth_height * self.width_depth_height))

        byte_index = int(index / 8.)
        bit_index = index - (byte_index * 8)

        if value:
            self.voxel_data[byte_index] = (
                self.voxel_data[byte_index]) | (0b1 << bit_index)
        else:
            self.voxel_data[byte_index] = (
                self.voxel_data[byte_index]) & ~(0b1 << bit_index)

    def get_voxel(self, x, y, z, width_depth_height=VH_MAX_WIDTH_DEPTH_HEIGHT):
        if width_depth_height != self.width_depth_height:
            self.resize(width_depth_height)

        return self.get_voxel_raw(x, y, z)

    def get_voxel_raw(self, x, y, z):
        index = int(x + (z * self.width_depth_height) +
                    (y * self.width_depth_height * self.width_depth_height))

        byte_index = int(index / 8.)
        bit_index = index - (byte_index * 8)

        return (self.voxel_data[byte_index]) & (0b1 << bit_index) != 0

    def set_voxel_color(self, x, y, z, value, width_depth_height=VH_MAX_WIDTH_DEPTH_HEIGHT):
        if width_depth_height != self.width_depth_height:
            self.resize(width_depth_height)

        self.set_voxel_color_raw(x, y, z, value)

    def set_voxel_color_raw(self, x, y, z, value):
        index = int(x + (z * self.width_depth_height) +
                    (y * self.width_depth_height * self.width_depth_height))

        self.color_table[index] = value

    def get_voxel_color(self, x, y, z, width_depth_height=VH_MAX_WIDTH_DEPTH_HEIGHT):
        if width_depth_height != self.width_depth_height:
            self.resize(width_depth_height)

        return self.get_voxel_color_raw(x, y, z)

    def get_voxel_color_raw(self, x, y, z):
        index = int(x + (z * self.width_depth_height) +
                    (y * self.width_depth_height * self.width_depth_height))

        return self.color_table[index]

    def to_bytes(self, compress=False):
        if compress:
            print("Currently not support compress voxel object.")

        data = bytes()

        # Write Position
        data += self.position.to_bytes()

        props = 0

        # Prepare Object Data
        if not compress:
            width_depth_height_n = get_lsb_number(self.width_depth_height)
            color_table_size = 0
            voxel_data = self.voxel_data
            color_table = bytes()

            for x in range(self.width_depth_height):
                for y in range(self.width_depth_height):
                    for z in range(self.width_depth_height):
                        if self.get_voxel_raw(x, y, z):
                            color_table += struct.pack("B", self.get_voxel_color_raw(x, y, z))
                            color_table_size += 1

        # Write Compressed
        if compress:
            props = props | VH_GEOMETRY_COMPRESSED_MASK
            props = props | VH_COLOR_TABLE_COMPRESSED_MASK

        # Write Color Table Size
        color_table_size = color_table_size & VH_COLOR_TABLE_SIZE_10BITS
        color_table_size = color_table_size << 4
        props = props | color_table_size

        # Write Destroyble
        if self.destroyable:
            props = props | VH_PROPERTY_DESTROYABLE_1BITS

        # Write Width Depth Height N
        width_depth_height_n = width_depth_height_n & VH_WIDTH_DEPTH_HEIGHT_2BITS
        props = props | width_depth_height_n

        # Write Properties
        data += int.to_bytes(props, 2, 'little', signed=False)

        # Write Owner Serial
        data += int.to_bytes(self.owner_serial, 8, 'little', signed=True)

        # Write Object Data
        data += voxel_data
        data += color_table

        return data

    @staticmethod
    def from_bytes(bytes, offset=0):
        if len(bytes) < 16:
            raise ValueError("VoxelObject size must be greater than 16 bytes.")

        # Read Position
        position = VoxelShortPosition.from_bytes(bytes[offset:offset + 6])
        offset += 6

        # Read Properties
        props = int.from_bytes(
            bytes[offset:offset + 2], 'little', signed=False)
        offset += 2

        # Read Compressed
        color_table_compressed = (props & VH_COLOR_TABLE_COMPRESSED_MASK) != 0
        geometry_compressed = (props & VH_GEOMETRY_COMPRESSED_MASK) != 0

        # Read Color Table Size
        color_table_size = (props & VH_COLOR_TABLE_SIZE_MASK) >> 4

        # Read Width Depth Height N
        width_depth_height_n = props & VH_WIDTH_DEPTH_HEIGHT_2BITS
        width_depth_height = int(math.pow(2, width_depth_height_n))

        instance = VoxelObject(width_depth_height=width_depth_height)
        instance.position = position

        if color_table_compressed:
            print("Currently not support decompress color table, skip color data of {0} object.".format(
                instance.position.__dict__))

            for i in range(int(math.pow(width_depth_height, 3))):
                instance.color_table[i] = 15
            # raise ValueError("Currently not support decompress color table.")

        if geometry_compressed:
            raise ValueError("Currently not support decompress voxel data.")

        # Read Destroyable
        instance.destroyable = (
            (props & VH_PROPERTY_DESTROYABLE_1BITS) >> 2) != 0

        # Read Owner Serial
        instance.owner_serial = int.from_bytes(
            bytes[offset:offset + 8], 'little', signed=True)
        offset += 8

        voxel_full_count = int(math.pow(width_depth_height, 3))
        voxel_data_size = int(voxel_full_count / 8 +
                              (voxel_full_count % 8 != 0))

        # Read Geometry Data
        if not geometry_compressed:
            instance.voxel_data = bytearray(bytes[offset:offset + voxel_data_size])
        offset += voxel_data_size

        # Read Color Table Data
        if not color_table_compressed:
            color_table = bytes[offset:offset + color_table_size]
            
            if len(color_table) != math.pow(instance.width_depth_height, 3):
                local_index = 0
                for y in range(instance.width_depth_height):
                    for z in range(instance.width_depth_height):
                        for x in range(instance.width_depth_height):
                            if instance.get_voxel_raw(x, y, z):
                                instance.set_voxel_color_raw(x, y, z, color_table[local_index])
                                local_index += 1
                            else:
                                instance.set_voxel_color_raw(x, y, z, 0)

                if len(color_table) != local_index:
                    raise ValueError("Unexpected color table structure.")
            else:
                instance.color_table = color_table

        offset += color_table_size

        return instance


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
        data = bytes()

        # Write Version
        data += int.to_bytes(VH_VOXEL_FILE_VERSION, 4, 'little', signed=False)

        # Write Object Count
        data += int.to_bytes(len(self.objects), 4, 'little', signed=False)

        # Write Light Count
        data += int.to_bytes(0, 4, 'little', signed=False)

        # Write White Point
        data += struct.pack('f', self.white_point)

        # Write Reserved
        data += bytes(4 * 15)

        stream_data = bytes()
        for object in self.get_objects():
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
