from chess_base import Position, Piece, COLOR
from chess_utils import prune_result


class Tower(Piece):
    def __init__(self, pos=Position(0, 0), color=COLOR.WHITE):
        super().__init__(pos, color, 'T')

    @prune_result
    def possible_moves(self, *args, **kwargs) -> list:
        return [Position(self.pos.x, i) for i in range(0, 8)] + [Position(i, self.pos.y) for i in range(0, 8)]

    @prune_result
    def attack_locations(self, *args, **kwargs) -> list:
        return self.possible_moves()

    def display(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    print(Tower().possible_moves())
