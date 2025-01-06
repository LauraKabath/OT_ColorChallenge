import random

from colors import *


class Grid:
    def __init__(self, screen, grid_size, cell_size):
        self.__screen = screen
        self.__size = grid_size
        self.__cell_size = cell_size
        # matrix representing playing area
        self.__grid = [[random.randint(1, 4) for _ in range(self.__size)] for _ in range(self.__size)]
        self.__selection = set()  # a set to store positions of selected blocks
        self.__full_size = self.__size * self.__cell_size
        self.__remaining_cells = self.__size**2  # number of cells/blocks in the grid

    def draw_grid(self):
        # draws blocks according to generated grid
        for row in range(self.__size):
            for col in range(self.__size):
                color = COLORS[self.__grid[row][col]]
                pg.draw.rect(self.__screen, color,
                             (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size))
                pg.draw.rect(self.__screen, (0, 0, 0),
                             (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size), 1)

    def select_block(self, row, col, color):
        # selects block of the same color using recursion
        if (row, col) in self.__selection or row < 0 or col < 0 or row >= self.__size or col >= self.__size:
            return
        if self.__grid[row][col] != color:
            return

        self.__selection.add((row, col))
        # recursion
        self.select_block(row - 1, col, color)  # up
        self.select_block(row + 1, col, color)  # down
        self.select_block(row, col - 1, color)  # left
        self.select_block(row, col + 1, color)  # right
        # not allowing selection of a single block
        if len(self.__selection) == 1:
            self.__selection.pop()

    def remove_blocks(self):
        # removes all blocks in the selection
        for row, col in self.__selection:
            self.__grid[row][col] = 0

        for col in range(self.__size):  # shifting blocks down
            column = [self.__grid[row][col] for row in range(self.__size)]
            column = [i for i in column if i != 0]  # removes empty spaces
            column = [0] * (self.__size - len(column)) + column  # adds empty spaces at the top
            for row in range(self.__size):  # updates grid
                self.__grid[row][col] = column[row]

        for col in range(self.__size - 1, -1, -1):  # from right to left
            if all([self.__grid[row][col] == 0 for row in range(self.__size)]):  # if the column is empty
                for shift_col in range(col, self.__size - 1):  # shifts empty column to the right
                    for row in range(self.__size):
                        self.__grid[row][shift_col] = self.__grid[row][shift_col + 1]
                for row in range(self.__size): # the rightest column will be emptied
                    self.__grid[row][self.__size - 1] = 0

        self.update_remaining_cells(len(self.__selection))
        self.clear_selection()

    def highlight_selection(self):
        for row, col in self.__selection:
            color = HIGHLIGHT_COLORS[self.__grid[row][col]]
            pg.draw.rect(self.__screen, color,
                         (col * self.__cell_size, row * self.__cell_size, self.__cell_size, self.__cell_size))

    def regenerate(self):
        self.__grid.clear()
        self.clear_selection()
        self.__remaining_cells = self.__size**2
        self.__grid = [[random.randint(1, 4) for _ in range(self.__size)] for _ in range(self.__size)]
        self.draw_grid()

    def remove_color(self, color):
        self.clear_selection()
        # selection when DELETE color_btn is clicked
        for row in range(self.__size):
            for col in range(self.__size):
                if self.__grid[row][col] == color:
                    self.__selection.add((row, col))

        count = self.get_selection_count()
        self.remove_blocks()
        return count

    def boost_selection(self, row, col):
        self.clear_selection()
        self.__selection.add((row, col))
        # selection when boost-bomb is used
        if (row + 1) < self.__size and self.__grid[row + 1][col] != 0:
            self.__selection.add((row + 1, col))  # down
        if (row - 1) >= 0 and self.__grid[row - 1][col] != 0:
            self.__selection.add((row - 1, col))  # up
        if (col + 1) < self.__size and self.__grid[row][col + 1] != 0:
            self.__selection.add((row, col + 1))  # right
        if (col - 1) >= 0 and self.__grid[row][col - 1] != 0:
            self.__selection.add((row, col - 1))  # left

    def thunder_color(self, color):
        near = False
        self.clear_selection()
        # random selection of blocks to change color
        row_selection = [random.randint(1, self.__size - 1) for _ in range(self.__size // 2)]
        col_selection = [random.randint(1, self.__size - 1) for _ in range(2)]
        for row in row_selection:
            for col in col_selection:
                if self.__grid[row][col] != 0 and self.__grid[row][col] != color:
                    self.__grid[row][col] = color
                    near = True

        self.draw_grid()
        return near

    def get_cell(self, row, col):
        return self.__grid[row][col]

    def get_selection(self):
        return self.__selection

    def get_selection_count(self):
        return len(self.__selection)

    def get_full_size(self):
        return self.__full_size

    def get_remaining_cells(self):
        return self.__remaining_cells

    def update_remaining_cells(self, count):
        self.__remaining_cells -= count

    def clear_selection(self):
        self.__selection.clear()
