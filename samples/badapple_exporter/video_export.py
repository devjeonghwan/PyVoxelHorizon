import cv2
from pyvoxelhorizon.voxel import *

video = cv2.VideoCapture("badapple.mp4")
count = 0

while True:
    _, image = video.read()

    if image is None:
        print("Done!")
        break

    original_height, original_width, _ = image.shape
    image = cv2.resize(image, (original_width // 4, original_height // 4), interpolation=cv2.INTER_CUBIC)
    height, width, _ = image.shape
    
    voxel_file = VoxelFile()
    voxel_file.white_point = 1.0

    offset_x = 0
    offset_y = -6
    offset_z = 0

    for y in range(height):
        for x in range(width):
            color = image[(height - 1 - y), x]
            
            color_index = find_similar_color(color[2], color[1], color[0])

            # 이미지를 8x8 단위로 읽어내면 Object 얻어오는 비용을 줄일 수 있을 것
            object = voxel_file[offset_x + (x // 8), offset_y + (y // 8), offset_z]
            
            local_x = x % 8
            local_y = y % 8

            object.set_voxel(local_x, local_y, 0, True)
            object.set_voxel_color(local_x, local_y, 0, color_index)

    file = open("frames/%d.vxl" % count, "wb")
    file.write(voxel_file.to_bytes())
    file.close()

    count = count + 1