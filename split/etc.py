from itertools import chain
from chess import Cursor, Chess


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
