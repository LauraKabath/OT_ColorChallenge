import random

from colors import *
from cube import GroupGrid, Cube
from animated_boosts import Thunder, Boom, Explosion


class Grid:
    def __init__(self, screen, grid_size, cell_size):
        self.__screen = screen
        self.__size = grid_size
        self.__cell_size = cell_size
        # groups
        self.__group = GroupGrid()
        self.__cubes_group = pg.sprite.Group()
        self.__thunders_group = pg.sprite.Group()
        self.__booms_group = pg.sprite.Group()
        self.__explosions_group = pg.sprite.Group()
        # matrix representing playing area
        self.__grid = [[random.randint(1, 4) for _ in range(self.__size)] for _ in range(self.__size)]
        self.__cubeGrid = [
            [Cube(self.__screen, col * self.__cell_size, row * self.__cell_size, self.__cell_size,
                  self.__grid[row][col], (self.__group, self.__cubes_group))
             for col in range(self.__size)]
            for row in range(self.__size)
        ]
        self.__selection = set()  # a set to store positions of selected blocks
        self.__full_size = self.__size * self.__cell_size
        self.__remaining_cells = self.__size**2  # number of cells/blocks in the grid
        # thunder boost attributes
        self.__thunder_activated = False
        self.__thunder_array = []
        # boom, explosion boost attributes
        self.__explosion_activated = False
        self.__explosion_array = []
        self.__boom_array = []

    def draw_grid(self, delta):
        # draws cubes according to generated grid
        pg.draw.rect(self.__screen, COLORS[0], (0, 0, self.__full_size, self.__full_size))
        for row in range(self.__size):
            for col in range(self.__size):
                cube = self.__cubeGrid[row][col]
                self.__highlight_selection()
                if cube:
                    self.__cubeGrid[row][col].draw()

        if len(self.__boom_array) != 0:
            for boom in self.__boom_array:
                boom.draw_boom(delta)

        self.__thunder_activation(delta)
        self.__explosion_activation(delta)

    def __thunder_activation(self, delta):
        if self.__thunder_activated and len(self.__thunder_array) > 0:
            for thunder in self.__thunder_array:
                thunder.draw_thunder(delta)
            if self.__thunder_array[0].disappear():
                self.__thunder_activated = False
                self.__thunder_color(self.__thunder_array[0].get_color())
                self.__thunder_array.clear()
        else:
            self.__thunder_activated = False

    def __explosion_activation(self, delta):
        if self.__explosion_activated and len(self.__explosion_array) > 0:
            for boom in self.__boom_array:
                boom.kill()
            self.__boom_array.clear()
            for exp in self.__explosion_array:
                exp.draw_explosion(delta)
            if self.__explosion_array[0].get_state() == 8:
                self.remove_blocks()
                self.__explosion_activated = False
                self.__explosion_array.clear()
        else:
            self.__explosion_activated = False

    def select_block(self, row, col, color):
        # selects block of the same color using recursion
        if (row, col) in self.__selection or row < 0 or col < 0 or row >= self.__size or col >= self.__size:
            return
        if self.__grid[row][col] != color:
            return

        self.__selection.add((row, col))
        self.__cubeGrid[row][col].select()
        # recursion
        self.select_block(row - 1, col, color)  # up
        self.select_block(row + 1, col, color)  # down
        self.select_block(row, col - 1, color)  # left
        self.select_block(row, col + 1, color)  # right
        # not allowing selection of a single block
        if len(self.__selection) == 1:
            self.__cubeGrid[row][col].unselect()
            self.__selection.pop()

    def remove_blocks(self):
        # removes all blocks in the selection
        for row, col in self.__selection:
            self.__grid[row][col] = 0
            self.__cubeGrid[row][col] = None

        # handle falling blocks column by column
        for col in range(self.__size):
            column = [self.__grid[row][col] for row in range(self.__size)]
            column = [i for i in column if i != 0]  # removes empty spaces
            column = [0] * (self.__size - len(column)) + column  # adds empty spaces at the top
            # collects all non-None cubes in the column
            column_cubes = [self.__cubeGrid[row][col] for row in range(self.__size) if
                            self.__cubeGrid[row][col] is not None]
            missing_cubes = self.__size - len(column_cubes)

            for row in range(self.__size):  # updates grid
                self.__grid[row][col] = column[row]

            # shifts existing cubes down
            for row in range(len(column_cubes)):
                cube = column_cubes[row]
                new_row = missing_cubes + row
                new_y = new_row * self.__cell_size
                self.__cubeGrid[new_row][col] = cube
                cube.start_falling(new_y)  # falling animation

            # fills the top of the column with new cubes
            for row in range(missing_cubes):
                new_color = 0
                new_cube = Cube(
                    self.__screen,
                    col * self.__cell_size,
                    row * self.__cell_size,
                    self.__cell_size,
                    new_color,
                    (self.__group, self.__cubes_group)
                )
                self.__cubeGrid[row][col] = new_cube

        for s_col in range(self.__size - 1, -1, -1):  # from right to left
            if all([self.__grid[row][s_col] == 0 for row in range(self.__size)]):  # if the column is empty
                for shift_col in range(s_col, self.__size - 1):  # shifts empty column to the right
                    for row in range(self.__size):
                        x = shift_col * self.__cell_size
                        self.__grid[row][shift_col] = self.__grid[row][shift_col + 1]
                        self.__cubeGrid[row][shift_col] = self.__cubeGrid[row][shift_col + 1]
                        if self.__cubeGrid[row][shift_col] is not None:
                            self.__cubeGrid[row][shift_col].start_shifting(x)  # shifting animation
                for row in range(self.__size):  # the rightest column will be emptied
                    self.__grid[row][self.__size - 1] = 0
                    self.__cubeGrid[row][self.__size - 1] = None

        # update the score based on the number of removed blocks
        self.update_remaining_cells(len(self.__selection))
        self.clear_selection()

    def fall(self, delta):  # handles falling of all cubes in grid
        for row in range(self.__size):
            for col in range(self.__size):
                cube = self.__cubeGrid[row][col]
                if cube:
                    cube.fall(delta)

    def shift(self, delta):
        for row in range(self.__size):
            for col in range(self.__size):
                cube = self.__cubeGrid[row][col]
                if cube:
                    cube.shift(delta)

    def __highlight_selection(self):
        for row, col in self.__selection:
            self.__cubeGrid[row][col].select()

    def regenerate(self, level):
        self.__grid.clear()
        self.clear_selection()
        self.__remaining_cells = self.__size**2
        self.__grid = [[random.randint(1, self.__get_range(level)) for _ in range(self.__size)] for _ in
                       range(self.__size)]
        self.__cubeGrid = [
            [Cube(self.__screen, col * self.__cell_size, row * self.__cell_size, self.__cell_size,
                  self.__grid[row][col], (self.__group, self.__cubes_group))
             for col in range(self.__size)]
            for row in range(self.__size)
        ]

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
        # clearing previous selection
        self.clear_selection()
        self.clear_explosion()
        # directions for explosion
        destinations = [(row, col), (row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
        for destination in destinations:
            row = destination[0]
            col = destination[1]
            if 0 <= row < self.__size and 0 <= col < self.__size:
                if self.__grid[row][col] != 0:
                    self.__selection.add((row, col))
                    self.__cubeGrid[row][col].select()
                    self.__boom_array.append(Boom(self.__screen, (col * self.__cell_size, row * self.__cell_size),
                                                  (self.__group, self.__booms_group)))
                    self.__explosion_array.append(
                        Explosion(self.__screen, (col * self.__cell_size, row * self.__cell_size),
                                  (self.__group, self.__explosions_group)))

    def thunder_charge(self, color):
        near = False  # True - thunder stroked, False - thunder was far away
        self.__thunder_activated = True
        self.clear_selection()
        # random selection of blocks to change color
        row_selection = [random.randint(0, self.__size - 1) for _ in range(7)]
        col_selection = [random.randint(0, self.__size - 1) for _ in range(5)]
        for row in row_selection:
            for col in col_selection:
                if self.__grid[row][col] != 0 and self.__grid[row][col] != color:
                    near = True
                    self.__thunder_array.append(
                        Thunder(self.__screen, (col * self.__cell_size, row * self.__cell_size), color,
                                (self.__group, self.__thunders_group)))
        return near

    def __thunder_color(self, color):
        for thunder in self.__thunder_array:
            thunder_position = thunder.get_position()
            row = thunder_position[1] // self.__cell_size
            col = thunder_position[0] // self.__cell_size
            if self.__grid[row][col] != 0 and self.__grid[row][col] != color:
                self.__grid[row][col] = color
                self.__cubeGrid[row][col].change_color(color)

    def __count_color(self, color):
        color_count = 0
        for row in range(self.__size):
            color_count = len([self.__grid[row][col] for col in range(self.__size) if self.__grid[row][col] == color])
        return color_count

    def get_color_counts(self, level):
        color_arr = []
        for i in range(1, self.__get_range(level) + 1):
            color_arr.append(self.__count_color(i))
        return color_arr

    def __get_range(self, level):
        if 10 >= level > 5:
            return 5
        if level > 10:
            return 6
        return 4

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
        for row in range(self.__size):
            for col in range(self.__size):
                cube = self.__cubeGrid[row][col]
                if cube:
                    self.__cubeGrid[row][col].unselect()

    def clear_explosion(self):
        for boom in self.__boom_array:
            boom.kill()
        self.__boom_array.clear()

        for exp in self.__explosion_array:
            exp.kill()
        self.__explosion_array.clear()

    def get_thunder(self):
        return self.__thunder_activated

    def get_explosion(self):
        return self.__explosion_activated

    def activate_explosion(self):
        self.__explosion_activated = True
