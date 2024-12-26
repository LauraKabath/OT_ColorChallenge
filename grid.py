import pygame as pg
import random


class Grid:
    def __init__(self, screen, size, cell_size):
        self.__screen = screen
        self.__size = size
        self.__cell_size = cell_size
        self.__grid = [[random.randint(1, 4) for i in range(self.__size)] for j in range(self.__size)]
        self.__selection = set()
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
        for row in range(self.__size):
            for col in range(self.__size):
                color = self.__COLORS[self.__grid[row][col]]
                pg.draw.rect(self.__screen, color,
                             (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size))
                pg.draw.rect(self.__screen, (0, 0, 0),
                             (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size), 1)

    def select_block(self, row, col, color):
        if (row, col) in self.__selection or row < 0 or col < 0 or row >= self.__size or col >= self:
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

    def highlight_selection(self):
        for row, col in self.__selection:
            color = self.__HIGHLIGHT_COLORS[self.__grid[row][col]]
            pg.draw.rect(self.__screen, color,
                         (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size))

    def get_cell(self, row, col):
        return self.__grid[row][col]

    def get_selection(self):
        return self.__selection

    def clear_selection(self):
        self.__selection.clear()
