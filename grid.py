import pygame as pg
import random


class Grid:
    def __init__(self, screen, cell_count, cell_size):
        self.__screen = screen
        self.__cell_count = cell_count
        self.__cell_size = cell_size
        self.__grid = [[random.randint(1, 4) for i in range(self.__cell_count)] for j in range(self.__cell_count)]
        self.__selection = set()
        self.__size = self.__cell_count * self.__cell_size
        self.__COLORS = {
            0: (200, 200, 200),  # pozadie siva
            1: (255, 186, 0),  # zlta
            2: (182, 47, 47),  # cervena
            3: (93, 194, 3),  # zelena
            4: (11, 80, 183)  # modra
        }

        self.__HIGHLIGHT_COLORS = {
            1: (255, 207, 77),  # zlta highlight
            2: (212, 84, 84),  # cervena highlight
            3: (124, 223, 36),  # zelena highlight
            4: (36, 101, 198)  # modra highlight
        }

    def draw_grid(self):
        for row in range(self.__cell_count):
            for col in range(self.__cell_count):
                color = self.__COLORS[self.__grid[row][col]]
                pg.draw.rect(self.__screen, color,
                             (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size))
                pg.draw.rect(self.__screen, (0, 0, 0),
                             (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size), 1)

    def select_block(self, row, col, color):
        if (row, col) in self.__selection or row < 0 or col < 0 or row >= self.__cell_count or col >= self.__cell_count:
            return
        if self.__grid[row][col] != color:
            return

        self.__selection.add((row, col))
        self.select_block(row - 1, col, color)  # up
        self.select_block(row + 1, col, color)  # down
        self.select_block(row, col - 1, color)  # left
        self.select_block(row, col + 1, color)  # right

        if len(self.__selection) == 1:
            self.__selection.pop()

    def remove_blocks(self):
        for row, col in self.__selection:
            self.__grid[row][col] = 0

        for col in range(self.__cell_count):
            column = [self.__grid[row][col] for row in range(self.__cell_count)]
            column = [i for i in column if i != 0]
            column = [0] * (self.__cell_count - len(column)) + column
            for row in range(self.__cell_count):
                self.__grid[row][col] = column[row]

        for col in range(self.__cell_count - 1, -1, -1):
            if all([self.__grid[row][col] == 0 for row in range(self.__cell_count)]):
                for shift_col in range(col, self.__cell_count - 1):
                    for row in range(self.__cell_count):
                        self.__grid[row][shift_col] = self.__grid[row][shift_col + 1]
                for row in range(self.__cell_count):
                    self.__grid[row][self.__cell_count - 1] = 0

        self.clear_selection()

    def highlight_selection(self):
        for row, col in self.__selection:
            color = self.__HIGHLIGHT_COLORS[self.__grid[row][col]]
            pg.draw.rect(self.__screen, color,
                         (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size))

    def get_cell(self, row, col):
        return self.__grid[row][col]

    def get_selection(self):
        return self.__selection

    def get_size(self):
        return self.__size

    def clear_selection(self):
        self.__selection.clear()
