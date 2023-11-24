class Position:
    def __init__(self, pixels_x, pixels_y):
        self.x = pixels_x
        self.y = pixels_y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def add_x(self, pixels_x):
        self.x += pixels_x

    def add_y(self, pixels_y):
        self.y += pixels_y

    def set_x(self, pixels_x):
        self.x = pixels_x

    def set_y(self, pixels_y):
        self.y = pixels_y

    def update_pos(self, pixels_x, pixels_y):
        self.add_x(pixels_x)
        self.add_y(pixels_y)

    def get_position(self):
        return self.x, self.y