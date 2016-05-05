import curses
from itertools import chain
from copy import copy
from validator import Validator
from minions import Pawn, Rook, Knight, Bishop, Queen, King, Empty
from chess import screen, Cursor, Shell


class ChessClass(object):
    def __init__(self):
        self.board = [[Empty() for i in range(8)] for i in range(8)]
        self.draw_indexes()

    def init_pawns(self, nopawns=False):
        self.spawn_minion('white', 'rook', 0, 7)
        self.spawn_minion('white', 'knight', 1, 7)
        self.spawn_minion('white', 'bishop', 2, 7)
        self.spawn_minion('white', 'queen', 3, 7)
        self.spawn_minion('white', 'king', 4, 7)
        self.spawn_minion('white', 'bishop', 5, 7)
        self.spawn_minion('white', 'knight', 6, 7)
        self.spawn_minion('white', 'rook', 7, 7)
        self.spawn_minion('black', 'rook', 0, 0)
        self.spawn_minion('black', 'knight', 1, 0)
        self.spawn_minion('black', 'bishop', 2, 0)
        self.spawn_minion('black', 'queen', 3, 0)
        self.spawn_minion('black', 'king', 4, 0)
        self.spawn_minion('black', 'bishop', 5, 0)
        self.spawn_minion('black', 'knight', 6, 0)
        self.spawn_minion('black', 'rook', 7, 0)
        if nopawns is False:
            for i in range(8):
                self.spawn_minion('white', 'pawn', i, 6)
                self.spawn_minion('black', 'pawn', i, 1)

    def highlight_movable_fields(self, Pawn):
        a, b = Cursor.selected()
        moves = (0, 0)
        if Pawn.name is not 'empty':
            moves = chain.from_iterable(Pawn.valid_moves.values())
            moves = [(m[0] + a, m[1] + b) for m in moves]
            return moves
        return []

    def display(self):
        self.draw_indexes()
        moves = []
        if Cursor.sel:
            a, b = Cursor.selected()
            moves = self.highlight_movable_fields(self.board[b][a])
        for y in reversed(range(8)):
            for x in range(8):
                Minion = self.board[y][x]
                color = self.color_as_number(Minion)
                if (x, y) == Cursor.pointed():
                    screen.addstr(2 + y, 3 + (x * 2), Minion.symbol, curses.color_pair(color) | curses.A_BOLD)
                elif (x, y) == Cursor.selected():
                    screen.addstr(2 + y, 3 + (x * 2), Minion.symbol, curses.color_pair(4) | curses.A_BOLD)
                elif (x, y) in (moves):
                    screen.addstr(2 + y, 3 + (x * 2), Minion.symbol, curses.color_pair(9))
                else:
                    screen.addstr(2 + y, 3 + (x * 2), Minion.symbol, curses.color_pair(color))

    def move(self, x1, y1, x2, y2):
        Guardian = Validator(x1, y1, x2, y2)
        if Guardian.verdict() is True:
            tmp = copy(self.board[y1][x1])
            self.board[y2][x2] = tmp
            self.board[y1][x1] = Empty()
            Cursor.unselect()
            Shell.add_log('{0} Moved: {1} > {2}'.format(
                self.board[y2][x2].name, self.chess_notation(x1, y1), self.chess_notation(x2, y2)))
        del Guardian

    def move_valid(self, Pawn, x, y):
        return True

    def validate_direction(self, Pawn, x, y):
        pass

    def spawn_minion(self, color, name, x, y):
        if self.spawn_validation(color, name, x, y) is False:
            return False
        else:
            if name is 'rook':
                self.board[y][x] = Rook(color)
            elif name is 'bishop':
                self.board[y][x] = Bishop(color)
            elif name is 'queen':
                self.board[y][x] = Queen(color)
            elif name is 'knight':
                self.board[y][x] = Knight(color)
            elif name is 'king':
                self.board[y][x] = King(color)
            elif name is 'pawn':
                self.board[y][x] = Pawn(color)
            Shell.add_log('Created Minion: {0} {1} at {2}'.format(
                self.board[y][x].color, self.board[y][x].name, self.chess_notation(x, y)))
            return True

    def spawn_validation(self, color, name, x, y):
        if color not in ('white', 'black'):
            screen.addstr(13, 2, 'Invalid color')
            return False
        elif x * y < 0 or x > 7 or y > 7:
            screen.addstr(13, 2, 'Out of range')
            return False
        else:
            return True

    def color_as_number(self, Minion):
        if Minion.color is 'black':
            return 2
        elif Minion.color is 'white':
            return 3
        else:
            return 1

    def draw_indexes(self):
        for i in range(8):
            screen.addstr(1, 3 + (i * 2), chr(97 + i))  # 97 -> 'a' in ASCII code
            screen.addstr(10, 3 + (i * 2), chr(97 + i))
            screen.addstr(2 + i, 1, str(8 - i))
            screen.addstr(2 + i, 19, str(8 - i))

    def is_empty(self, field):
        """ expects to get coords tuple or pawn object """
        if type(field) is tuple:
            x, y = field
            return True if self.board[y][x].name in ('empty', 'Empty') else False
        else:
            return True if field.name in ('empty', 'Empty') else False

    def chess_notation(self, index_x, index_y):
        return ''.join([chr(97 + index_x), chr(8 - index_y + 48)])

    def index_notation(self, string):
        return [ord(string[0]) - 97, 8 - int(string[1])]
