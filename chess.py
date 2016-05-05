import curses
from copy import copy
from itertools import chain
# requires pympler
# from pympler.tracker import SummaryTracker

# !! CONSOLE NEEDS TO BE AT LEAST 77x11 !!


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
        """ checks if last field has different color """
        if self.target_color == self.Pawn.color:
            return False
        else:
            return True

    def verdict(self):
        if self.validate1() is True and self.validate2() is True and self.validate3() is True:
            return True
        else:
            return False


class ShellClass(object):
    def __init__(self):
        self.height = 9
        self.width = 36
        self.shift_x = 25
        self.shift_y = 2
        self.log = ['>' for i in range(self.height)]
        self.mode = 'Cursor'
        self.input = []

    def draw_log_border(self):
        for y in range(self.height):
            for x in range(self.width):
                screen.addstr(self.shift_y + y, self.shift_x + x, '*')

    def add_log(self, string=''):
        while len(string) > self.width:
            del(self.log[0])
            self.log.append(string[:self.width])
            string = string[self.width:]
        del(self.log[0])
        self.log.append(string)

    def display(self):
        screen.addstr(self.shift_y - 1, self.shift_x + 2, '{0} mode'.format(self.mode))
        for i, string in enumerate(self.log):
            screen.addstr(self.shift_y + i, self.shift_x, string)

    def print_info(self):
        self.add_log()
        self.add_log('wsad moves cursor')
        self.add_log("press 'g' to select field")
        self.add_log("press 'h' to move selected pawn to cursor current location")


###########################
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


###########################
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


###########################
class CursorClass(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.index_x = 0
        self.index_y = 0
        self.shift_x = 3
        self.shift_y = 2
        self.screen_size_x = 16
        self.screen_size_y = 8
        self.selected_x = None
        self.selected_y = None
        self.sel = False
        # self.symbol = '.'

    def move(self, delta_x, delta_y):
        self.x = (self.x + (delta_x) * 2) % self.screen_size_x
        self.y = (self.y - delta_y) % self.screen_size_y
        self.index_x = int(self.x / 2)
        self.index_y = self.y

    def show_selected_minion_moves(self):
        moves = Chess.board[self.index_y][self.index_x].valid_moves
        for i, key in enumerate(moves.keys()):
            screen.addstr(12, 3, 'Valid moves: ')
            screen.addstr(13 + i, 5, key)
            screen.addstr(13 + i, 8, str(moves[key]))

    def show_cursor_info(self):
        selected = Chess.board[self.index_y][self.index_x]
        screen.addstr(1, 62, 'console coords: ')
        screen.addstr(2, 62, '({0}, {1})'.format(self.x + self.shift_x, self.y + self.shift_y))
        screen.addstr(3, 62, 'board indexes: ')
        screen.addstr(4, 62, '({0}, {1})'.format(self.index_x, self.index_y))
        screen.addstr(5, 62, 'chess notation: ')
        screen.addstr(6, 62, '({0}, {1})'.format(chr(97 + self.index_x), 8 - self.index_y))
        screen.addstr(7, 62, selected.info())

    def display(self):
        # screen.addstr(self.y + self.shift_y, self.x + self.shift_x, self.symbol, curses.color_pair(3))
        self.show_cursor_info()
        # self.show_selected_minion_moves()

    def select(self):
        if (self.index_x, self.index_y) == (self.selected_x, self.selected_y):
            self.unselect()
        else:
            self.sel, self.selected_x, self.selected_y = True, self.index_x, self.index_y

    def unselect(self):
        self.sel, self.selected_x, self.selected_y = False, None, None

    def pointed(self):
        return (self.index_x, self.index_y)

    def selected(self):
        return (self.selected_x, self.selected_y)

    def any_selected(self):
        return self.sel


###########################
def key_manager(key, CursorClass):
    if key == ord('w'):
        Cursor.move(0, 1)
    elif key == ord('s'):
        Cursor.move(0, -1)
    elif key == ord('a'):
        Cursor.move(-1, 0)
    elif key == ord('d'):
        Cursor.move(1, 0)
    elif key == ord('g'):
        Cursor.select()
    elif key == ord('h'):
        if Cursor.any_selected() is True:
            Chess.move(*chain(Cursor.selected(), Cursor.pointed()))

###########################
# tracker = SummaryTracker()
screen = curses.initscr()
curses.start_color()
curses.use_default_colors()
curses.noecho()
curses.init_pair(1, curses.COLOR_WHITE, -1)
curses.init_pair(2, curses.COLOR_BLUE, -1)
curses.init_pair(3, curses.COLOR_RED, -1)
curses.init_pair(4, curses.COLOR_GREEN, -1)
curses.init_pair(9, curses.COLOR_CYAN, -1)
Shell = ShellClass()
Cursor = CursorClass()
Chess = ChessClass()
# Chess.spawn_minion('white', 'rook', 3, 5)
# Chess.spawn_minion('black', 'rook', 1, 4)
# Chess.spawn_minion('black', 'bishop', 0, 0)
# Chess.spawn_minion('black', 'rook', 7, 7)
# Chess.spawn_minion('white', 'bishop', 3, 0)
# Chess.spawn_minion('white', 'rook', 3, 1)
Chess.init_pawns(nopawns=True)
key = 'something'
Chess.display()
Shell.print_info()

try:
    while key != ord('p'):
        key = screen.getch()
        key_manager(key, Cursor)
        screen.clear()
        Shell.display()
        Chess.display()
        Cursor.display()
        screen.refresh()
finally:
    curses.endwin()
    # print('Pympler is working...')
    # tracker.print_diff()
