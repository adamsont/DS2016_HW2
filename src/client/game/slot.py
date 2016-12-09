__author__ = 'Taavi'


class Slot:
    EMPTY = 0
    HIT = 1
    MISS = 2
    SHIP = 3

    FIELD_SEPARATOR = ':'
    OBJ_SEPARATOR = '|'

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.state = self.EMPTY

    def to_string(self):
        return "Slot (" + str(self.x) + " : " + str(self.y) + ") s:" + str(self.state)

    def serialize(self):
        ser_str = str(self.x) + self.FIELD_SEPARATOR + str(self.y) + self.FIELD_SEPARATOR + str(self.state) + self.OBJ_SEPARATOR
        return ser_str