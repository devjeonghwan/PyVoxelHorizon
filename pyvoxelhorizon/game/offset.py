GLOBAL_OFFSET = {
    'STATIC': {
        'GAME': 0x00140148
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
        'MOUSE_RIGHT_BUTTON_DOWN'       : 0x00000BE8
    },
    'FUNCTION': {

    }
}

SCENE_OFFSET = {
    'FIELD': {
    },
    'FUNCTION': {
        'LOAD_VOXELS': 0x000899B0
    }
}