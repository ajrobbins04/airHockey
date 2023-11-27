class Position:
    def __init__(self, pixels_x, pixels_y):
        self._x = pixels_x
        self._y = pixels_y

    def get_x(self):
        return self._x
    
    def get_y(self):
        return self._y
    
    def add_x(self, pixels_x):
        self._x += pixels_x

    def add_y(self, pixels_y):
        self._y += pixels_y

    def set_x(self, pixels_x):
        self._x = pixels_x

    def set_y(self, pixels_y):
        self._y = pixels_y

    def update_pos(self, pixels_x, pixels_y):
        self.add_x(pixels_x)
        self.add_y(pixels_y)

    def get_position(self):
        return self._x, self._y