from time import sleep
import cv2
import numpy
from pyvoxelhorizen import *

import pymeow

voxel_file = VoxelFile.from_file("big.vxl")

min_x = 99999999
min_y = 99999999
min_z = 99999999

max_x = -99999999
max_y = -99999999
max_z = -99999999

for object in voxel_file.get_objects():
    min_x = min(object.position.x, min_x)
    min_y = min(object.position.y, min_y)
    min_z = min(object.position.z, min_z)
    
    max_x = max(object.position.x, max_x)
    max_y = max(object.position.y, max_y)
    max_z = max(object.position.z, max_z)

length_x = abs(max_x - min_x) + 1
length_y = abs(max_y - min_y) + 1
length_z = abs(max_z - min_z) + 1

print("Calculated voxel object size. {0}x{1}x{2}".format(length_x, length_y, length_z))

width = int(length_x * VH_MAX_WIDTH_DEPTH_HEIGHT)
height = int(length_z * VH_MAX_WIDTH_DEPTH_HEIGHT)

print("Final image size = {0}x{1}".format(width, height))

layers = []
lines = []
for layer_index in range(min_y, max_y + 1):
    for y_index in range(VH_MAX_WIDTH_DEPTH_HEIGHT):
        layers.append(numpy.zeros((height, width, 3), dtype=numpy.uint8))
        lines.append(numpy.zeros((height, width, 1), dtype=numpy.uint8))

print("Prepared all layers.")

layer_index = 0
for object_y in range(min_y, max_y + 1):
    local_y = (object_y - min_y) * 8
    voxel_y = 0
    current_object = None

    for voxel_y in range(VH_MAX_WIDTH_DEPTH_HEIGHT):
        print("Start render {0} layer.".format(layer_index))

        for object_z in range(min_z, max_z + 1):
            for object_x in range(min_x, max_x + 1):
                current_object = voxel_file.get_object(object_x, object_y, object_z)

                local_x = (object_x - min_x) * 8
                local_z = (object_z - min_z) * 8

                if current_object is not None:
                    width_depth_height = current_object.width_depth_height
                    resolution = int(VH_MAX_WIDTH_DEPTH_HEIGHT / width_depth_height)
                    local_layer_index = local_y + (voxel_y * resolution)

                    if voxel_y < width_depth_height:
                        for voxel_z in range(width_depth_height):
                            for voxel_x in range(width_depth_height):
                                if current_object.get_voxel_raw(voxel_x, voxel_y, voxel_z):
                                    color_index = current_object.get_voxel_color_raw(voxel_x, voxel_y, voxel_z)
                                    color = VH_COLORS[color_index]

                                    current_x = int(local_x + (voxel_x * resolution))
                                    current_z = int(local_z + (voxel_z * resolution))
                                    
                                    for res in range(resolution):
                                        lines[local_layer_index + res][current_z:current_z+resolution, current_x:current_x+resolution, 0] = 255

                                        layers[local_layer_index + res][current_z:current_z+resolution, current_x:current_x+resolution, 0] = color.blue
                                        layers[local_layer_index + res][current_z:current_z+resolution, current_x:current_x+resolution, 1] = color.green
                                        layers[local_layer_index + res][current_z:current_z+resolution, current_x:current_x+resolution, 2] = color.red
        
        layer_index += 1

print("Merging layers.")

rescale_ratio = 2
line_width = 3
line_interval = 3

kernel = numpy.ones((line_width, line_width), numpy.uint8)

rescaled_width = width * rescale_ratio
rescaled_height = height * rescale_ratio
image = numpy.zeros((rescaled_height, rescaled_width, 3), dtype=numpy.uint8)

for index in range(len(layers)):
    print("Start merge {0} layer.".format(index))
    
    if index % line_interval == 0:
        line = cv2.resize(lines[index], (rescaled_width, rescaled_height), interpolation=cv2.INTER_NEAREST)

        line = cv2.dilate(line, kernel, iterations=1)
        line = numpy.stack((line, line, line), axis=2)

        line_mask = line > 0
        image[line_mask] = 0

    layer = cv2.resize(layers[index], (rescaled_width, rescaled_height), interpolation=cv2.INTER_NEAREST)

    layer_mask = layer > 0
    image[layer_mask] = layer[layer_mask]


print("Waiting process..")

process = None

while process is None:
    try:
        process = pymeow.process_by_name('Client_x64_release.exe')
    except:
        print("Retry..")
    sleep(1)

base_address = process["modules"]["Client_x64_release.exe"]["baseaddr"] + 0x00137AA8

print("Attached process.")

def read_offsets(process, base_address, offsets):
    base_point = pymeow.read_int64(process, base_address)

    current_pointer = base_point

    for i in offsets[:-1]:
        current_pointer = pymeow.read_int64(process, current_pointer + i)

    return current_pointer + offsets[-1]

x_pointer = None
y_pointer = None
z_pointer = None

while True:
    try:
        x_pointer = read_offsets(process, base_address, [0x630, 0x320, 0x20, 0xA0, 0x40, 0x90, 0x60])
        y_pointer = read_offsets(process, base_address, [0x630, 0x320, 0x20, 0xA0, 0x40, 0x90, 0x64])
        z_pointer = read_offsets(process, base_address, [0x630, 0x320, 0x20, 0xA0, 0x40, 0x90, 0x68])
        break
    except:
        print("Waiting for connect server..")
        sleep(1)

while process is not None:
    try:
        x = pymeow.read_float(process, x_pointer)
        z = pymeow.read_float(process, z_pointer)
        
        canvas = image.copy()

        object_x = int(x / 400.0)
        object_z = int(z / 400.0)
        
        voxel_x = int((x - int(object_x * 400)) / 50.0)
        voxel_z = int((z - int(object_z * 400)) / 50.0)
        
        image_x = ((object_x - min_x) * VH_MAX_WIDTH_DEPTH_HEIGHT) + voxel_x
        image_z = ((object_z - min_z) * VH_MAX_WIDTH_DEPTH_HEIGHT) + voxel_z

        if image_x >= 0 and image_x < width:
            if image_z >= 0 and image_z < height:
                image_x *= rescale_ratio
                image_z *= rescale_ratio
                image_x = int(image_x)
                image_z = int(image_z)
                cv2.circle(canvas, (image_x, image_z), 8, (0, 0, 255), -1)

        cv2.imshow("MAP", canvas)
        cv2.waitKey(10)
    except Exception as e:
        print(e)
        print("Waiting for join map..")
        sleep(1)
