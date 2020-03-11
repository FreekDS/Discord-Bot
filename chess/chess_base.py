import enum
from abc import abstractmethod


class Position:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        return None if (x or y) not in range(0, 8) else Position(x, y)

    def __str__(self):
        return "({}, {})".format(self.x, self.y)

    def __repr__(self):
        return str(self)


class COLOR(enum.Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, pos=Position(), color: COLOR = COLOR.WHITE, string_repr="0"):
        self.color = color
        self.string_repr = string_repr
        self.pos = pos
        self._made_first_move = False

    def set_pos(self, new_pos, *args, **kwargs):
        self.pos = new_pos
        self._made_first_move = True

    @abstractmethod
    def possible_moves(self, *args, **kwargs) -> list:
        return []

    @abstractmethod
    def attack_locations(self, *args, **kwargs) -> list:
        return []

    def __str__(self):
        return self.string_repr

    @abstractmethod
    def display(self, *args, **kwargs):
        pass

    def has_moved(self):
        return self._made_first_move

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    p = Position(0, 0)
    p2 = Position(7, 7)
    print(p + p2)
