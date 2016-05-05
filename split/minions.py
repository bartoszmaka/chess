class Minion(object):
    def __init__(self, color=None):
        self.color = color
        # self.valid_moves = {}
        self.define_valid_moves_mask()

    def info(self):
        return ', '.join(map(str, [self.name, self.color]))

    # def __del__(self):
    #     try:
    #         Shell.add_log('Deleted {0}'.format(self.name))
    #     except Exception:
    #         pass
    #         # print('Deleted {0}'.format(self.name))


########################
class Empty(Minion):
    def __init__(self):
        self.define_valid_moves_mask()
        self.color = None
        self.name = 'empty'
        self.symbol = '#'

    def define_valid_moves_mask(self):
        self.valid_moves = {}


########################
class Rook(Minion):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'rook'
        self.symbol = 'R'

    def define_valid_moves_mask(self):
        self.valid_moves = {'N': [], 'S': [], 'E': [], 'W': []}
        for i in range(1, 8):
            self.valid_moves['N'].append((0, -i))
            self.valid_moves['E'].append((i, 0))
            self.valid_moves['S'].append((0, i))
            self.valid_moves['W'].append((-i, 0))


###########################
class Bishop(Minion):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'bishop'
        self.symbol = 'B'

    def define_valid_moves_mask(self):
        self.valid_moves = {'NE': [], 'SE': [], 'NW': [], 'SW': []}
        for i in range(1, 8):
            self.valid_moves['NE'].append((i, -i))
            self.valid_moves['SE'].append((i, i))
            self.valid_moves['NW'].append((-i, -i))
            self.valid_moves['SW'].append((-i, i))


###########################
class King(Minion):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'king'
        self.symbol = 'W'

    def define_valid_moves_mask(self):
        self.valid_moves = {'N': [], 'S': [], 'E': [], 'W': [], 'NE': [], 'SE': [], 'NW': [], 'SW': []}
        for i in range(1, 2):
            self.valid_moves['N'].append((0, -i))
            self.valid_moves['E'].append((i, 0))
            self.valid_moves['S'].append((0, i))
            self.valid_moves['W'].append((-i, 0))
            self.valid_moves['NE'].append((i, -i))
            self.valid_moves['SE'].append((i, i))
            self.valid_moves['NW'].append((-i, -i))
            self.valid_moves['SW'].append((-i, i))


###########################
class Queen(Minion):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'queen'
        self.symbol = 'Q'

    def define_valid_moves_mask(self):
        self.valid_moves = {'N': [], 'S': [], 'E': [], 'W': [], 'NE': [], 'SE': [], 'NW': [], 'SW': []}
        for i in range(1, 8):
            self.valid_moves['N'].append((0, -i))
            self.valid_moves['E'].append((i, 0))
            self.valid_moves['S'].append((0, i))
            self.valid_moves['W'].append((-i, 0))
            self.valid_moves['NE'].append((i, -i))
            self.valid_moves['SE'].append((i, i))
            self.valid_moves['NW'].append((-i, -i))
            self.valid_moves['SW'].append((-i, i))


###########################
class Pawn(Minion):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'pawn'
        self.symbol = 'P'

    def define_valid_moves_mask(self):
        self.valid_moves = {}
        if self.color is 'white':
            self.valid_moves['N'] = [(0, -1)]
        else:
            self.valid_moves['S'] = [(0, 1)]


###########################
class Knight(Minion):
    def __init__(self, color):
        super().__init__(color)
        self.name = 'knight'
        self.symbol = 'K'

    def define_valid_moves_mask(self):
        self.valid_moves = {'N': [], 'S': [], 'E': [], 'W': [], 'NE': [], 'SE': [], 'NW': [], 'SW': []}
        self.valid_moves['N'] = [(1, 2)]
        self.valid_moves['E'] = [(2, 1)]
        self.valid_moves['S'] = [(2, -1)]
        self.valid_moves['W'] = [(1, -2)]
        self.valid_moves['NE'] = [(-1, -2)]
        self.valid_moves['SE'] = [(-2, -1)]
        self.valid_moves['NW'] = [(-2, 1)]
        self.valid_moves['SW'] = [(-1, 2)]
