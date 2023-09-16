from pyvoxelhorizon import *
from pyanvil import World, BlockState, Material

voxel_file = VoxelFile()
voxel_file.white_point = 1.0

offset_x = -30
offset_y = -6
offset_z = -30

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

def simd_voxel(object, x, y, z, bools, colors):
    single_color = not isinstance(colors, list)

    for index in range(len(simd_order)):
        offset = simd_order[index]

        if bools[index]:
            object.set_voxel(x + offset[0], y + offset[1], z + offset[2], True)

            if single_color:
                object.set_voxel_color(x + offset[0], y + offset[1], z + offset[2], colors)
            else:
                object.set_voxel_color(x + offset[0], y + offset[1], z + offset[2], colors[index])

def make_stairs_shape(half, facing, shape):
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
    
    return datas

def make_slab_shape(type):
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
    
    return datas
    

with World('C:/Users/devpa/AppData/Roaming/.minecraft/saves/IvyWood Manor', debug=False) as wolor:
    start_mc_x = -120
    end_mc_x = 124
    
    start_mc_y = 57
    end_mc_y = 100

    start_mc_z = 12
    end_mc_z = 150

# with World('C:/Users/devpa/AppData/Roaming/.minecraft/saves/New World', debug=False) as wolor:
#     start_mc_x = -120
#     end_mc_x = -103
    
#     start_mc_y = 1
#     end_mc_y = 4

#     start_mc_z = -56
#     end_mc_z = -45

# with World('C:/Users/devpa/AppData/Roaming/.minecraft/saves/A2', debug=False) as wolor:
#     start_mc_x = -50
#     end_mc_x = -20
    
#     start_mc_y = 1
#     end_mc_y = 4

#     start_mc_z = 40
#     end_mc_z = 65

    mc_vh_color_map = {
        'minecraft:red_wool': 29,
        'minecraft:blue_wool': 20,
        'minecraft:white_wool': 16,

        'minecraft:coal_block': 11,
        'minecraft:black_concrete': 11,
        'minecraft:white_concrete': 16,
        'minecraft:light_gray_concrete': 15,
        'minecraft:glowstone': 6,

        'minecraft:smooth_quartz': 16,
        'minecraft:smooth_quartz_slab': 16,

        'minecraft:jungle_stairs': 11,
        'minecraft:jungle_leaves': 48,
        'minecraft:jungle_slab': 11,
        'minecraft:jungle_planks': [11, 11, 10, 10, 11, 11, 10, 10],
        'minecraft:jungle': [11, 11, 10, 10, 11, 11, 10, 10],
        'minecraft:jungle_log': [11, 10, 11, 10, 11, 10, 11, 10],
        'minecraft:jungle_wood': 11,
        'minecraft:jungle_trapdoor': 10,

        'minecraft:spruce_stairs': 0,
        'minecraft:spruce_leaves': 48,
        'minecraft:spruce_slab': 0,
        'minecraft:spruce_planks': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:spruce': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:spruce_log': [1, 0, 1, 0, 1, 0, 1, 0],
        'minecraft:spruce_wood': 0,
        'minecraft:spruce_trapdoor': 0,

        'minecraft:dark_oak_stairs': 0,
        'minecraft:dark_oak_leaves': 48,
        'minecraft:dark_oak_slab': 0,
        'minecraft:dark_oak_planks': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:dark_oak': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:dark_oak_log': [1, 0, 1, 0, 1, 0, 1, 0],
        'minecraft:dark_oak_wood': 0,
        'minecraft:dark_oak_trapdoor': 0,

        'minecraft:petrified_oak_stairs': 1,
        'minecraft:petrified_oak_leaves': 48,
        'minecraft:petrified_oak_slab': 1,
        'minecraft:petrified_oak_planks': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:petrified_oak': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:petrified_oak_log': [1, 0, 1, 0, 1, 0, 1, 0],
        'minecraft:petrified_oak_wood': 1,
        'minecraft:petrified_oak_trapdoor': 1,
        
        'minecraft:oak_stairs': 1,
        'minecraft:oak_leaves': 48,
        'minecraft:oak_slab': 1,
        'minecraft:oak_planks': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:oak': [1, 1, 0, 0, 1, 1, 0, 0],
        'minecraft:oak_log': [1, 0, 1, 0, 1, 0, 1, 0],
        'minecraft:oak_wood': 1,
        'minecraft:oak_trapdoor': 1,
        
        'minecraft:birch_stairs': 14,
        'minecraft:birch_leaves': 47,
        'minecraft:birch_slab': 14,
        'minecraft:birch_planks': [14, 14, 15, 15, 14, 14, 15, 15],
        'minecraft:birch': [14, 14, 15, 15, 14, 14, 15, 15],
        'minecraft:birch_log': [14, 13, 14, 15, 13, 14, 15, 14],
        'minecraft:birch_wood': 14,
        'minecraft:birch_trapdoor': 14,

        'minecraft:light_gray': 13,

        'minecraft:andesite': 36,
        'minecraft:andesite_wall': 36,

        'minecraft:diorite': 52,
        'minecraft:diorite_wall': 52,

        'minecraft:sandstone': 60,
        'minecraft:sandstone_wall': 60,
        'minecraft:sand': 6,

        'minecraft:smooth_stone': 38,
        'minecraft:smooth_stone_stairs': 38,
        'minecraft:smooth_stone_slab': 38,

        'minecraft:smooth_sandstone': 60,
        'minecraft:smooth_sandstone_stairs': 60,
        'minecraft:smooth_sandstone_slab': 60,

        'minecraft:nether_brick': 29,
        'minecraft:nether_brick_stairs': 29,
        'minecraft:nether_brick_slab': 29,

        'minecraft:stone': 52,
        'minecraft:stone_stairs': 52,
        'minecraft:stone_slab': 52,
        
        'minecraft:granite': 36,

        'minecraft:gravel': 56,
        'minecraft:iron_ore': 52,
        'minecraft:coal_ore': 52,
        
        'minecraft:iron_block': 41,
        'minecraft:gold_block': 6,
        'minecraft:emerald_block': 9,
        'minecraft:diamond_block': 18,

        'minecraft:grass_block': 47,
        'minecraft:dirt': 50,
        
        'minecraft:iron_bars': 41,
        'minecraft:heavy_weighted_pressure_plate': 16,
        'minecraft:blast_furnace': [11, 11, 11, 11, 12, 12, 12, 12],
        
        'minecraft:azure_bluet': 6,
        'minecraft:dandelion': 6,
        'minecraft:oxeye_daisy': 7,
        'minecraft:cornflower': 19,
        'minecraft:poppy': 28,
        'minecraft:dead_bush': 1,
        'minecraft:lily_of_the_valley': 16,
        
        'minecraft:potted_azure_bluet': 6,
        'minecraft:potted_dandelion': 6,
        'minecraft:potted_oxeye_daisy': 7,
        'minecraft:potted_cornflower': 19,
        'minecraft:potted_poppy': 28,
        'minecraft:potted_dead_bush': 1,
        'minecraft:potted_lily_of_the_valley': 16,

        'minecraft:flower_pot': 1,

        'minecraft:water': 42
    }

    mc_vh_shape_map = {
        'minecraft:andesite_wall': [False, False, False, False, True, True, True, True],
        'minecraft:diorite_wall': [False, False, False, False, True, True, True, True],
        'minecraft:sandstone_wall': [False, False, False, False, True, True, True, True],

        'minecraft:iron_bars': [True, False, False, True, True, False, False, True],
        'minecraft:heavy_weighted_pressure_plate': [False, False, False, False, True, True, True, True],

        'minecraft:azure_bluet': [False, False, False, False, True, False, False, False],
        'minecraft:dandelion': [False, False, False, False, True, False, False, False],
        'minecraft:oxeye_daisy': [False, False, False, False, False, True, False, False],
        'minecraft:cornflower': [False, False, False, False, False, False, True, False],
        'minecraft:poppy': [False, False, False, False, False, False, False, True],
        'minecraft:dead_bush': [False, False, False, False, True, False, False, False],
        'minecraft:lily_of_the_valley': [True, True, False, False, True, False, False, False],
        
        'minecraft:potted_azure_bluet': [False, False, False, False, True, False, False, False],
        'minecraft:potted_dandelion': [False, False, False, False, True, False, False, False],
        'minecraft:oxeye_daisy': [False, False, False, False, False, True, False, False],
        'minecraft:potted_cornflower': [False, False, False, False, False, False, True, False],
        'minecraft:potted_poppy': [False, False, False, False, False, False, False, True],
        'minecraft:potted_dead_bush': [False, False, False, False, True, False, False, False],
        'minecraft:potted_lily_of_the_valley': [True, True, False, False, True, False, False, False],

        'minecraft:flower_pot': [False, False, False, False, True, False, False, False]
    }
    
    mc_ignores = [
        'grass',
        'glass',
        'glass_pane',
        'fern',
        'air',
        'sign',
        'lever',
        'button',
        'ladder',
        'campfire',
        'carpet',
        'head',
        'hook',
        'torch',
        'door',
        'cobweb',
        'cauldron',
        'bed',
        'bookshelf',
        'lantern',
        'fence',
        'sapling',
        'banner',
        'rod',
        'table',
        'stand',
    ]

    for mc_y in range((end_mc_y - start_mc_y) + 1):
        for mc_z in range((end_mc_z - start_mc_z) + 1):
            for mc_x in range((end_mc_x - start_mc_x) + 1):
                try:
                    mc_block = wolor.get_block((start_mc_x + mc_x, start_mc_y + mc_y, start_mc_z + mc_z))
                    mc_block_name = mc_block.get_state().name
                    mc_block_props = mc_block.get_state().props

                    vh_color = None

                    if mc_block_name in mc_vh_color_map:
                        vh_color = mc_vh_color_map[mc_block_name]

                    if vh_color is not None:
                        if vh_color != -1:
                            object_x = int(mc_x / 4)
                            object_y = int(mc_y / 4)
                            object_z = int(mc_z / 4)
                            
                            voxel_x = int(mc_x % 4) * 2
                            voxel_y = int(mc_y % 4) * 2
                            voxel_z = int(mc_z % 4) * 2

                            object = voxel_file[offset_x + object_x, offset_y + object_y, offset_z + object_z]

                            if mc_block_name.endswith('_stairs'):
                                half = mc_block_props["half"]
                                facing = mc_block_props["facing"]
                                shape = mc_block_props["shape"]

                                simd_voxel(object, voxel_x, voxel_y, voxel_z, make_stairs_shape(half, facing, shape), vh_color)
                            elif mc_block_name.endswith('_slab'):
                                type = mc_block_props["type"]
                                
                                simd_voxel(object, voxel_x, voxel_y, voxel_z, make_slab_shape(type), vh_color)
                            else:
                                if mc_block_name in mc_vh_shape_map:
                                    simd_voxel(object, voxel_x, voxel_y, voxel_z, mc_vh_shape_map[mc_block_name], vh_color)
                                else:
                                    simd_voxel(object, voxel_x, voxel_y, voxel_z, [True, True, True, True, True, True, True, True], vh_color)
                    else:
                        excepted = False
                        for ignore in mc_ignores:
                            if mc_block_name.endswith(ignore):
                                excepted = True
                                break
                            
                        if not excepted:
                            print(mc_block_name)
                            print("\t" + str(mc_block_props))
                except Exception as e:
                    I = 0
                    # print("IGNORE " + str((start_mc_x + mc_x, start_mc_y + mc_y, start_mc_z + mc_z)), e)
                
file = open("datas/output.vxl", "wb")
file.write(voxel_file.to_bytes())
file.close()