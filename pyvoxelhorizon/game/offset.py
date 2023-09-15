# for 20230906 Build 33

GLOBAL_OFFSET = {
    'STATIC': {
        'GAME': 0x00142158
    }
}

GAME_OFFSET = {
    'FIELD': {
        'WINDOW_WIDTH'                  : 0x00000008,
        'WINDOW_HEIGHT'                 : 0x0000000C,
        'DEVICE_WIDTH'                  : 0x00000010,
        'DEVICE_HEIGHT'                 : 0x00000014,

        'SCENE'                         : 0x00000628,
        
        'IS_IN_PRIVATE_MAP'             : 0x00000BD4,
        'IS_IN_PVP_MODE'                : 0x00000BD8,

        'MOUSE_LEFT_BUTTON_DOWN'        : 0x00000BE0,
        'MOUSE_MIDDLE_BUTTON_DOWN'      : 0x00000BE4,
        'MOUSE_RIGHT_BUTTON_DOWN'       : 0x00000BE8,

        'VOXEL_EDITOR'                  : 0x000007E0,
    },
    'FUNCTION': {
        'WRITE_TEXT'                    : 0x0005A120
    }
}

SCENE_OFFSET = {
    'FIELD': {
    },
    'FUNCTION': {
    }
}

BATTLE_SCENE_OFFSET = {
    'FIELD': {
        'VOXEL_OBJECT_MANAGER'          : 0x000040F8,
    },
    'FUNCTION': {
        'LOAD_VOXELS'                   : 0x0008AC50
    }
}

VOXEL_OBJECT_MANAGER_OFFSET = {
    'VIRTUAL_FUNCTION_TABLE': {
        'VOXEL_OBJECT_MANAGER': {
            'OFFSET'                                : 0x00000000,
            'FUNCTION': {
                "CREATE_VOXEL_OBJECT"               : 0x00000010,
                "GET_VOXEL_OBJECT_WITH_FLOAT_COORD" : 0x00000148,
                "UPDATE_VISIBILITY"                 : 0x00000370,
            }
        },
        'UNKNOWN_INTERFACE': {
            'OFFSET'                                : 0x00000008,
            'FUNCTION': {
            }
        }
    },
    'FIELD': {
    },
    'FUNCTION': {
    }
}

VOXEL_OBJECT_OFFSET = {
    'VIRTUAL_FUNCTION_TABLE': {
        'VOXEL_OBJECT': {
            'OFFSET'                                : 0x00000000,
            'FUNCTION': {
                "UPDATE_GEOMETRY"                   : 0x000000B0,
                "UPDATE_LIGHTING"                   : 0x000000B8,
                
                "GET_VOXEL_OBJECT_PROPERTY"         : 0x00000078,

                "GET_VOXEL"                         : 0x000000C0,
                "ADD_VOXEL_WITH_AUTO_RESIZE"        : 0x000000F0,
                "REMOVE_VOXEL_WITH_AUTO_RESIZE"     : 0x000000F8,

                "SET_VOXEL_COLOR_WITH_AUTO_RESIZE"  : 0x00000108,
                "SET_PALETTE_WITH_INDEXED_COLOR"    : 0x00000148,

                "SET_DESTROYABLE"                   : 0x000001A8,
                "IS_DESTROYABLE"                    : 0x000001B0,
            }
        }
    },
    'FIELD': {
    },
    'FUNCTION': {
    }
}