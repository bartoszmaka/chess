from chess import Chess, screen


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
