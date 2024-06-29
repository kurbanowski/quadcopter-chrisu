class Transmitter:
    def __init__(self, x, y, r):
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.r = r  # range
        self.connected = False  # is connected to start_point

    def __repr__(self):
        return f"x={self.x} y={self.y} r={self.r}"

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def is_in_range(self, x, y, r):
        distance = (x - self.x) ** 2 + (y - self.y) ** 2
        return distance < (self.r + r) ** 2
