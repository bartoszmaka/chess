from chess import Chess


class Validator(object):
    def __init__(self, x1, y1, x2, y2):
        self.Pawn = Chess.board[y1][x1]
        self.target_color = Chess.board[y2][x2].color
        self.dir = None
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.moves = {}
        self.apply_mask()

    def apply_mask(self):
        for key, value in self.Pawn.valid_moves.items():
            self.moves[key] = [(v[0] + self.x1, v[1] + self.y1) for v in value]

    def validate1(self):
        """ checks if pawn is allowed to move like this """
        for key in self.moves.keys():
            if (self.x2, self.y2) in self.moves[key]:
                self.dir = key
                return True
        else:
            return False

    def validate2(self):
        """ checks for collisions between pawn and target """
        if self.dir is not None:
            i = self.moves[self.dir].index((self.x2, self.y2))
            for field in self.moves[self.dir][:i]:
                if not Chess.is_empty(field):
                    return False
            else:
                return True
        return False

    def validate3(self):
        """ checks if target field is not pawn with same color """
        if self.target_color == self.Pawn.color:
            return False
        else:
            return True

    def verdict(self):
        if self.validate1() is True and self.validate2() is True and self.validate3() is True:
            return True
        else:
            return False
