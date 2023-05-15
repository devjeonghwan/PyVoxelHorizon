VH_WIDTH_DEPTH_HEIGHT_2BITS = 0b11
VH_PROPERTY_2BITS = 0b1100
VH_PROPERTY_DESTROYABLE_1BITS = 0b0100
VH_PROPERTY_RESERVED_1BITS = 0b1000
VH_COLOR_TABLE_SIZE_10BITS = 0b1111111111
VH_COLOR_TABLE_SIZE_MASK = VH_COLOR_TABLE_SIZE_10BITS << 4
VH_COLOR_TABLE_COMPRESSED_MASK = 0b1 << 14
VH_GEOMETRY_COMPRESSED_MASK = 0b1 << 15

VH_VOXEL_FILE_VERSION = 7
VH_MAX_WIDTH_DEPTH_HEIGHT = 8
VH_DEFAULT_WIDTH_DEPTH_HEIGHT = 8

class Color:
    def __init__(self, id, rgb=None, description=None):
        self.id = id

        if rgb is None:
            self.rgb = None
        else:
            self.rgb = rgb

        if description is None:
            description = "RGB(" + str(self.rgb) + ")"

        self.description = description

VH_COLORS = [
    Color(0, rgb=(71, 45, 60)),
    Color(1, rgb=(94, 54, 67)),
    Color(2, rgb=(122, 68, 74)),
    Color(3, rgb=(160, 91, 83)),
    Color(4, rgb=(191, 121, 88)),
    Color(5, rgb=(238, 161, 96)),
    Color(6, rgb=(244, 204, 161)),
    Color(7, rgb=(182, 213, 60)),
    Color(8, rgb=(113, 170, 52)),
    Color(9, rgb=(57, 123, 68)),
    Color(10, rgb=(60, 89, 86)),
    Color(11, rgb=(48, 44, 46)),
    Color(12, rgb=(90, 83, 83)),
    Color(13, rgb=(125, 112, 113)),
    Color(14, rgb=(160, 147, 142)),
    Color(15, rgb=(207, 198, 184)),

    Color(16, rgb=(223, 246, 245)),
    Color(17, rgb=(138, 235, 241)),
    Color(18, rgb=(40, 204, 223)),
    Color(19, rgb=(57, 120, 168)),
    Color(20, rgb=(57, 71, 120)),
    Color(21, rgb=(57, 49, 75)),
    Color(22, rgb=(86, 64, 100)),
    Color(23, rgb=(142, 71, 140)),
    Color(24, rgb=(205, 96, 147)),
    Color(25, rgb=(255, 174, 182)),
    Color(26, rgb=(244, 180, 27)),
    Color(27, rgb=(244, 126, 27)),
    Color(28, rgb=(230, 72, 46)),
    Color(29, rgb=(169, 59, 59)),
    Color(30, rgb=(130, 112, 148)),
    Color(31, rgb=(79, 84, 107)),

    Color(32, description="Green Grass"),
    Color(33, description="Dark Green Grass"),
    Color(34, description="Mud"),
    Color(35, description="Dirt1"),
    Color(36, description="Dirt2"),
    Color(37, description="Stone"),
    Color(38, description="Smooth Stone"),
    Color(39, description="Tile1"),
    Color(40, description="Tile2"),
    Color(41, description="Quartz"),
    Color(42, description="Blue Wool"),
    Color(43, description="Rock1"),
    Color(44, description="Rock2"),
    Color(45, description="Rock3"),
    Color(46, description="Check"),

    Color(47, description="Mat Green Grass"),
    Color(48, description="Mat Dark Green Grass"),
    Color(49, description="Mat Mud"),
    Color(50, description="Mat Dirt1"),
    Color(51, description="Mat Dirt2"),
    Color(52, description="Mat Stone"),
    Color(53, description="Mat Smooth Stone"),
    Color(54, description="Mat Tile1"),
    Color(55, description="Mat Tile2"),
    Color(56, description="Mat Quartz"),
    Color(57, description="Mat Blue Wool"),
    Color(58, description="Mat Rock1"),
    Color(59, description="Mat Rock2"),
    Color(60, description="Mat Rock3"),
    Color(61, description="Mat Check"),

    Color(62, description="Shining Check1"),
    Color(63, description="Shining Check2")
]

def find_similar_color(red, green, blue):
    find_distance = 255 * 255 * 255
    find_id = None

    for index in range(len(VH_COLORS)):
        color = VH_COLORS[index]

        if color.rgb != None:
            distance = (abs(
                color.rgb[0] - red) + abs(color.rgb[1] - green) + abs(color.rgb[2] - blue)) / 3

            if find_distance > distance:
                find_distance = distance
                find_id = color.id

    return find_id

def get_lsb_number(n):
    count = 0

    while True:
        if n <= 1:
            return count

        n = n >> 1
        count = count + 1