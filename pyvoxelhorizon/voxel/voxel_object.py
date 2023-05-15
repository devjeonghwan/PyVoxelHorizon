import math
import struct

from .constant import *

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

    def is_empty(self):
        for z in range(self.width_depth_height):
            for y in range(self.width_depth_height):
                for x in range(self.width_depth_height):
                    if self.get_voxel_raw(x, y, z):
                        return False

        return True

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

            for y in range(self.width_depth_height):
                for z in range(self.width_depth_height):
                    for x in range(self.width_depth_height):
                        if self.get_voxel_raw(x, y, z):
                            color_table += struct.pack("B",
                                                       self.get_voxel_color_raw(x, y, z))
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
        instance.destroyable = ((props & VH_PROPERTY_DESTROYABLE_1BITS) >> 2) != 0

        # Read Owner Serial
        instance.owner_serial = int.from_bytes(
            bytes[offset:offset + 8], 'little', signed=True)
        offset += 8

        voxel_full_count = int(math.pow(width_depth_height, 3))
        voxel_data_size = int(voxel_full_count / 8 +
                              (voxel_full_count % 8 != 0))

        # Read Geometry Data
        if not geometry_compressed:
            instance.voxel_data = bytearray(
                bytes[offset:offset + voxel_data_size])
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
                                instance.set_voxel_color_raw(
                                    x, y, z, color_table[local_index])
                                local_index += 1
                            else:
                                instance.set_voxel_color_raw(x, y, z, 0)

                if len(color_table) != local_index:
                    raise ValueError("Unexpected color table structure.")
            else:
                instance.color_table = color_table

        offset += color_table_size

        return instance