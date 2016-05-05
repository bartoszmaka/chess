from chess import screen


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
