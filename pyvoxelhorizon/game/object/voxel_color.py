class VoxelColor:
    id              : int        = None
    rgb             : tuple[int] = None
    description     : str        = None

    def __init__(self, id: int, rgb: tuple[int] = None, description: str = None):
        self.id = id

        if rgb is None:
            self.rgb = None
        else:
            self.rgb = rgb

        if description is None:
            description = "RGB(" + str(self.rgb) + ")"

        self.description = description

VOXEL_COLORS = [
    VoxelColor(0, rgb=(71, 45, 60)),
    VoxelColor(1, rgb=(94, 54, 67)),
    VoxelColor(2, rgb=(122, 68, 74)),
    VoxelColor(3, rgb=(160, 91, 83)),
    VoxelColor(4, rgb=(191, 121, 88)),
    VoxelColor(5, rgb=(238, 161, 96)),
    VoxelColor(6, rgb=(244, 204, 161)),
    VoxelColor(7, rgb=(182, 213, 60)),
    VoxelColor(8, rgb=(113, 170, 52)),
    VoxelColor(9, rgb=(57, 123, 68)),
    VoxelColor(10, rgb=(60, 89, 86)),
    VoxelColor(11, rgb=(48, 44, 46)),
    VoxelColor(12, rgb=(90, 83, 83)),
    VoxelColor(13, rgb=(125, 112, 113)),
    VoxelColor(14, rgb=(160, 147, 142)),
    VoxelColor(15, rgb=(207, 198, 184)),

    VoxelColor(16, rgb=(223, 246, 245)),
    VoxelColor(17, rgb=(138, 235, 241)),
    VoxelColor(18, rgb=(40, 204, 223)),
    VoxelColor(19, rgb=(57, 120, 168)),
    VoxelColor(20, rgb=(57, 71, 120)),
    VoxelColor(21, rgb=(57, 49, 75)),
    VoxelColor(22, rgb=(86, 64, 100)),
    VoxelColor(23, rgb=(142, 71, 140)),
    VoxelColor(24, rgb=(205, 96, 147)),
    VoxelColor(25, rgb=(255, 174, 182)),
    VoxelColor(26, rgb=(244, 180, 27)),
    VoxelColor(27, rgb=(244, 126, 27)),
    VoxelColor(28, rgb=(230, 72, 46)),
    VoxelColor(29, rgb=(169, 59, 59)),
    VoxelColor(30, rgb=(130, 112, 148)),
    VoxelColor(31, rgb=(79, 84, 107)),

    VoxelColor(32, description="Green Grass"),
    VoxelColor(33, description="Dark Green Grass"),
    VoxelColor(34, description="Mud"),
    VoxelColor(35, description="Dirt1"),
    VoxelColor(36, description="Dirt2"),
    VoxelColor(37, description="Stone"),
    VoxelColor(38, description="Smooth Stone"),
    VoxelColor(39, description="Tile1"),
    VoxelColor(40, description="Tile2"),
    VoxelColor(41, description="Quartz"),
    VoxelColor(42, description="Blue Wool"),
    VoxelColor(43, description="Rock1"),
    VoxelColor(44, description="Rock2"),
    VoxelColor(45, description="Rock3"),
    VoxelColor(46, description="Check"),

    VoxelColor(47, description="Mat Green Grass"),
    VoxelColor(48, description="Mat Dark Green Grass"),
    VoxelColor(49, description="Mat Mud"),
    VoxelColor(50, description="Mat Dirt1"),
    VoxelColor(51, description="Mat Dirt2"),
    VoxelColor(52, description="Mat Stone"),
    VoxelColor(53, description="Mat Smooth Stone"),
    VoxelColor(54, description="Mat Tile1"),
    VoxelColor(55, description="Mat Tile2"),
    VoxelColor(56, description="Mat Quartz"),
    VoxelColor(57, description="Mat Blue Wool"),
    VoxelColor(58, description="Mat Rock1"),
    VoxelColor(59, description="Mat Rock2"),
    VoxelColor(60, description="Mat Rock3"),
    VoxelColor(61, description="Mat Check"),

    VoxelColor(62, description="Shining Check1"),
    VoxelColor(63, description="Shining Check2")
]

VOXEL_COLOR_RGB_CACHE = {}

def find_similar_voxel_color(red, green, blue):
    key = str(red) + "_" + str(green) + "_" + str(blue)

    if not key in VOXEL_COLOR_RGB_CACHE:
        find_distance = 255 * 255 * 255
        find_color = None

        for index in range(len(VOXEL_COLORS)):
            color = VOXEL_COLORS[index]

            if color.rgb != None:
                distance = (abs(color.rgb[0] - red) + abs(color.rgb[1] - green) + abs(color.rgb[2] - blue)) / 3

                if find_distance > distance:
                    find_distance = distance
                    find_color = color
                
        VOXEL_COLOR_RGB_CACHE[key] = find_color

    return VOXEL_COLOR_RGB_CACHE[key]

def get_voxel_color(index):
    if index > 0 or index <= len(VOXEL_COLORS):
        return VOXEL_COLORS[0]
    
    return VOXEL_COLORS[index]