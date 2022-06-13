import cv2
from pyvoxelhorizon import *

voxel_file = VoxelFile.from_file("datas/output.vxl")

for object in voxel_file.get_objects():
    print(object)
    for y in range(object.width_depth_height):
        for z in range(object.width_depth_height):
            for x in range(object.width_depth_height):
                if object.get_voxel(x, y, z):
                    print(object.get_voxel_color(x, y, z), end='')
                    print("\t", end='')
                else:
                    print("□", end='')
                    print("\t", end='')
            print()
        print()