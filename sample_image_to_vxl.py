import cv2
from pyvoxelhorizen import *

image = cv2.imread("input.png")
height, width, _ = image.shape

voxel_file = VoxelFile()
voxel_file.white_point = 1.0

offset_x = 0
offset_y = -6
offset_z = 0

for y in range(height):
    for x in range(width):
        color = image[y, (width - 1 - x)]
        
        color_index = find_similar_color(color[2], color[1], color[0])

        # 이미지를 8x8 단위로 읽어내면 Object 얻어오는 비용을 줄일 수 있을 것
        object = voxel_file[offset_x + int(x / 8), offset_y, offset_z + int(y / 8)]
        
        local_x = y % 8
        local_z = x % 8

        object.set_voxel(local_x, 0, local_z, True)
        object.set_voxel_color(local_x, 0, local_z, color_index)

file = open("out.vxl", "wb")
file.write(voxel_file.to_bytes())
file.close()