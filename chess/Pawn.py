from chess_base import Piece, COLOR, Position
from chess_utils import prune_result


class Pawn(Piece):
    def __init__(self, pos=Position(), color: COLOR = COLOR.WHITE):
        super().__init__(pos, color, "P")

    @prune_result
    def possible_moves(self, pieces) -> list:
        if self.color == COLOR.WHITE:
            positions = [self.pos + Position(0, 1)]
            if not self._made_first_move:
                positions.append(self.pos() + Position(0, 2))
            return positions
        else:
            positions = [self.pos + Position(0, -1)]
            if not self._made_first_move:
                positions.append(self.pos() + Position(0, -2))
            return positions

    @prune_result
    def attack_locations(self, *args, **kwargs) -> list:
        if self.color == COLOR.WHITE:
            return [self.pos + Position(1, 1), self.pos + Position(-1, 1)]
        else:
            return [self.pos + Position(1, -1), self.pos + Position(-1, -1)]

    def promote(self):
        return Piece(self.pos, self.color)

    def display(self, *args, **kwargs):
        pass


if __name__ == '__main__':
    p = Pawn(Position(0, 0), COLOR.BLACK)
    p.attack_locations()
