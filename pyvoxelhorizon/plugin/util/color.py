class Color:
    red: int
    green: int
    blue: int
    alpha: int

    def __init__(self, red: int, green: int, blue: int, alpha: int = 255):
        red = min(max(red, 0), 255)
        green = min(max(green, 0), 255)
        blue = min(max(blue, 0), 255)
        alpha = min(max(alpha, 0), 255)

        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def get_rgb(self) -> int:
        return (self.red << 16) + (self.green << 8) + self.blue

    def get_bgr(self) -> int:
        return (self.blue << 16) + (self.green << 8) + self.red

    def get_rgba(self) -> int:
        return (self.red << 24) + (self.green << 16) + (self.blue << 8) + self.alpha

    def get_argb(self) -> int:
        return (self.alpha << 24) + (self.red << 16) + (self.green << 8) + self.blue

    def get_bgra(self) -> int:
        return (self.blue << 24) + (self.green << 16) + (self.red << 8) + self.alpha

    def get_abgr(self) -> int:
        return (self.alpha << 24) + (self.blue << 16) + (self.green << 8) + self.red
