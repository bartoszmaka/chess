import curses

from shell import ShellClass
from board import ChessClass
from cursor import CursorClass
from etc import key_manager


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
