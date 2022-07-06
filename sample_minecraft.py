from pyvoxelhorizon import *
from pyanvil import World, BlockState, Material

voxel_file = VoxelFile()
voxel_file.white_point = 1.0

offset_x = 0
offset_y = -6
offset_z = 0

simd_order = [
    (0, 1, 0),
    (1, 1, 0),
    (0, 1, 1),
    (1, 1, 1),
    (0, 0, 0),
    (1, 0, 0),
    (0, 0, 1),
    (1, 0, 1)
]
def simd_voxel(object, x, y, z, datas, color=None):
    for index in range(len(simd_order)):
        offset = simd_order[index]

        if color is None:
            data = datas[index]

            if data[0]:
                object.set_voxel(x + offset[0], y + offset[1], z + offset[2], True)
                object.set_voxel_color(x + offset[0], y + offset[1], z + offset[2], data[1])
        else:
            if datas[index]:
                object.set_voxel(x + offset[0], y + offset[1], z + offset[2], True)
                object.set_voxel_color(x + offset[0], y + offset[1], z + offset[2], color)


with World('C:/Users/devpa/AppData/Roaming/.minecraft/saves/New World', debug=False) as wolor:
    start_mc_x = -120
    end_mc_x = -103
    
    start_mc_y = 1
    end_mc_y = 4

    start_mc_z = -56
    end_mc_z = -45

# with World('C:/Users/devpa/AppData/Roaming/.minecraft/saves/A2', debug=False) as wolor:
#     start_mc_x = -50
#     end_mc_x = -20
    
#     start_mc_y = 1
#     end_mc_y = 4

#     start_mc_z = 40
#     end_mc_z = 65

    for mc_y in range((end_mc_y - start_mc_y) + 1):
        for mc_z in range((end_mc_z - start_mc_z) + 1):
            for mc_x in range((end_mc_x - start_mc_x) + 1):
                mc_block = wolor.get_block((start_mc_x + mc_x, start_mc_y + mc_y, start_mc_z + mc_z))
                mc_block_name = mc_block.get_state().name
                mc_block_props = mc_block.get_state().props

                if mc_block_name != "minecraft:air":
                    print(mc_block_name)
                    print("   " + str(mc_block_props))
                    object_x = int(mc_x / 4)
                    object_y = int(mc_y / 4)
                    object_z = int(mc_z / 4)
                    
                    object = voxel_file[offset_x + object_x, offset_y + object_y, offset_z + object_z]

                    voxel_x = int(mc_x % 4) * 2
                    voxel_y = int(mc_y % 4) * 2
                    voxel_z = int(mc_z % 4) * 2
                    
                    color = 46

                    if mc_block_name.startswith('minecraft:spruce'):
                        color = 0
                    elif mc_block_name.startswith('minecraft:oak'):
                        color = 1
                    elif mc_block_name.startswith('minecraft:birch'):
                        color = 15
                    elif mc_block_name.startswith('minecraft:stone'):
                        color = 37
                    elif mc_block_name.startswith('minecraft:smooth_stone'):
                        color = 38
                    elif mc_block_name.startswith('minecraft:light_gray'):
                        color = 13


                    if mc_block_name.endswith('_stairs'):
                        half = mc_block_props["half"]
                        facing = mc_block_props["facing"]
                        shape = mc_block_props["shape"]

                        datas = None

                        if half == 'bottom':
                            datas = [
                                False, False,
                                False, False,

                                True, True,
                                True, True
                            ]
                        else:
                            datas = [
                                True, True,
                                True, True,

                                False, False,
                                False, False
                            ]
                        
                        if shape == 'inner_left':
                            datas[3] = True
                            datas[1] = True
                            datas[2] = True

                            datas[7] = True
                            datas[5] = True
                            datas[6] = True
                        elif shape == 'inner_right':
                            datas[0] = True
                            datas[2] = True
                            datas[3] = True

                            datas[4] = True
                            datas[6] = True
                            datas[7] = True
                        elif shape == 'outer_left':
                            datas[2] = True
                            datas[6] = True
                        elif shape == 'outer_right':
                            datas[3] = True
                            datas[7] = True
                        else:
                            datas[2] = True
                            datas[3] = True
                            datas[6] = True
                            datas[7] = True

                        if facing == 'south':
                            datas = [
                                datas[0], datas[1], 
                                datas[3], datas[2], 
                                
                                datas[4], datas[5], 
                                datas[7], datas[6]
                            ]
                        elif facing == 'west':
                            datas = [
                                datas[3], datas[0], 
                                datas[2], datas[1], 
                                
                                datas[7], datas[4], 
                                datas[6], datas[5]
                            ]
                        elif facing == 'north':
                            datas = [
                                datas[2], datas[3], 
                                datas[1], datas[0], 
                                
                                datas[6], datas[7], 
                                datas[5], datas[4]
                            ]
                        elif facing == 'east':
                            datas = [
                                datas[1], datas[2], 
                                datas[0], datas[3], 
                                
                                datas[5], datas[6], 
                                datas[4], datas[7]
                            ]
                        
                        simd_voxel(object, voxel_x, voxel_y, voxel_z, datas, color)
                    elif mc_block_name.endswith('_slab'):
                        type = mc_block_props["type"]

                        datas = None

                        if type == 'bottom':
                            datas = [
                                False, False,
                                False, False,

                                True, True,
                                True, True
                            ]
                        else:
                            datas = [
                                True, True,
                                True, True,

                                False, False,
                                False, False
                            ]
                        
                        simd_voxel(object, voxel_x, voxel_y, voxel_z, datas, color)
                    else:
                        simd_voxel(object, voxel_x, voxel_y, voxel_z, [True, True, True, True, True, True, True, True], color)

file = open("datas/output.vxl", "wb")
file.write(voxel_file.to_bytes())
file.close()