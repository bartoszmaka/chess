import curses
from copy import copy
from itertools import chain
# requires pympler
# from pympler.tracker import SummaryTracker

# Console window needs to be at least 80x17 !


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

    # def input(self):
    #     self.mode = 'Input'
    #     key = None
    #     while key is not 27:    # ESC
    #         if key is 127:      # Backspace
    #             try:
    #                 self.input.pop()
    #             except IndexError:
    #                 pass
    #         else:
    #             self.input.append(chr(key))
    #     self.mode = 'Cursor'


###########################
class ChessClass(object):
    def __init__(self):
        self.board = [[Empty() for i in range(8)] for i in range(8)]
        self.draw_indexes()

    def init_pawns(self):
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
        for i in range(8):
            self.spawn_minion('white', 'pawn', i, 6)
            self.spawn_minion('black', 'pawn', i, 1)

    def move_valid(self, x1, y1, x2, y2):
        screen.addstr(12, 1, 'Validating move...')
        moves = self.board[y1][x1].valid_moves
        delta = (x2 - x1, y2 - y1)
        for direction, fields in moves.items():
            if delta in fields:
                index = fields.index(delta)
                return fields[:index]
                if self.collision(fields[:index]) is False and self.last_field_stuff(x1, y1, x2, y2) is True:
                    return True
        else:
            screen.addstr(13, 2, 'Move is not valid')
            return False

    def collision(self, fields):
        for field in fields[:-1]:
            if not field.is_empty():
                screen.addstr(14, 2, 'Collision detected')
                return True
        else:
            return False

    def last_field_stuff(self, x1, y1, x2, y2):
        target = self.board[y2][x2]
        current = self.board[y1][x1]
        if target.empty() is False and target.color is current.color:
            return False
        else:
            return True

    def is_empty(field):
        return True if field.name in ('empty', 'Empty') else False

    def spawn_minion(self, color, name, x, y):
        if self.spawn_validation(color, name, x, y) is False:
            return False
        else:
            if name is 'rook' or name is 'Rook':
                self.board[y][x] = Rook(color)
                Shell.add_log('Created Minion: {0} {1} at {2}'.format(
                    self.board[y][x].color, self.board[y][x].name, self.chess_notation(x, y)))
                return True

    def spawn_validation(self, color, name, x, y):
        if color not in ('white', 'White', 'black', 'Black'):
            screen.addstr(17, 2, 'Invalid color')
            return False
        elif name not in (
                'Rook', 'rook', 'Bishop', 'bishop', 'Knight', 'knight',
                'Queen', 'queen', 'King', 'king', 'Pawn', 'pawn'):
            screen.addstr(17, 2, 'Invalid minion name')
            return False
        elif x * y < 0 or x > 7 or y > 7:
            screen.addstr(17, 2, 'Out of range')
            return False
        else:
            return True

    def move(self, x1, y1, x2, y2):
        if self.move_valid(x1, y1, x2, y2):
            tmp = copy(self.board[y1][x1])
            self.board[y2][x2] = tmp
            self.board[y1][x1] = Empty()
            Cursor.unselect()
            Shell.add_log('{0} Moved: {1} > {2}'.format(self.board[y2][x2].name, self.chess_notation(x1, y1), self.chess_notation(x2, y2)))
        else:
            screen.addstr(19, 2, 'Niedozwolony ruch')

    def display(self):
        self.draw_indexes()
        for y in reversed(range(8)):
            for x in range(8):
                Minion = self.board[y][x]
                color = self.color_as_number(Minion)
                if (x, y) == Cursor.pointed():
                    screen.addstr(2 + y, 3 + (x * 2), Minion.symbol, curses.color_pair(color) | curses.A_BOLD)
                elif (x, y) == Cursor.selected():
                    screen.addstr(2 + y, 3 + (x * 2), Minion.symbol, curses.color_pair(4) | curses.A_BOLD)
                else:
                    screen.addstr(2 + y, 3 + (x * 2), Minion.symbol, curses.color_pair(color))

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

    def chess_notation(self, index_x, index_y):
        return ''.join([chr(97 + index_x), chr(8 - index_y + 48)])

    def index_notation(self, string):
        return [ord(string[0]) - 97, 8 - int(string[1])]


###########################
class Minion(object):
    def __init__(self, color=None):
        self.color = color
        self.define_valid_moves_mask()

    def info(self):
        return ', '.join(map(str, [self.name, self.color]))

    def __del__(self):
        try:
            Shell.add_log('Deleted {0}'.format(self.name))
        except Exception:
            pass
            # print('Deleted {0}'.format(self.name))


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
        self.define_valid_moves_mask()
        self.symbol = 'R'

    def define_valid_moves_mask(self):
        self.valid_moves = {'N': [], 'S': [], 'E': [], 'W': []}
        for i in range(8):
            self.valid_moves['N'].append((-i, 0))
            self.valid_moves['E'].append((i, 0))
            self.valid_moves['S'].append((0, i))
            self.valid_moves['W'].append((0, -i))


###########################
class CursorClass(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.index_x = 0
        self.index_y = 0
        self.shift_x = 3
        self.shift_y = 2
        # self.symbol = '.'
        self.screen_size_x = 16
        self.screen_size_y = 8
        self.selected_x = None
        self.selected_y = None
        self.sel = False

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
        self.show_selected_minion_moves()

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
curses.init_pair(9, curses.COLOR_BLACK, -1)
Shell = ShellClass()
Cursor = CursorClass()
Chess = ChessClass()
Chess.spawn_minion('white', 'rook', 3, 5)
Chess.spawn_minion('black', 'rook', 1, 4)
Chess.spawn_minion('black', 'rook', 0, 0)
Chess.spawn_minion('black', 'rook', 7, 7)
Chess.spawn_minion('white', 'rook', 3, 0)
Chess.spawn_minion('white', 'rook', 3, 1)
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
