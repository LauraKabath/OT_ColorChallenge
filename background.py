import random

from colors import *
from cube import Cube, GroupGrid


class Background:
    def __init__(self, screen, size):
        self.__screen = screen
        self.__cube_size = size
        # groups
        self.__group = GroupGrid()
        self.__cubes_group = pg.sprite.Group()
        self.__cubes = []
        # width - number of columns, height - number of rows
        self.__width = self.__screen.get_width() // self.__cube_size
        self.__height = self.__screen.get_height() // self.__cube_size
        # time attributes
        self.__time_next = 0  # time until the next cube appears
        self.__interval = 10  # time in seconds between appearances
        self.__A_speed = 100  # animation speed
        self.__max_count = 15  # maximum cubes on screen

    def draw_frame(self):
        self.__screen.fill(MX_BLUE_GREEN)
        for row in range(self.__height):
            for col in range(self.__width):
                if row == 0 or col == 0 or row == self.__height - 1 or col == self.__width - 1:
                    color = random.randint(1, 4)
                    cube = Cube(self.__screen, col * self.__cube_size, row * self.__cube_size, self.__cube_size, color,
                                (self.__group, self.__cubes_group))
                    self.__cubes.append(cube)
        self.__draw_cubes()

    def draw_animated_background(self, delta, color=0):
        self.__screen.fill(MX_BLUE_GREEN)
        self.__time_next += delta * self.__A_speed
        if self.__time_next >= self.__interval and len(self.__cubes) < self.__max_count:
            self.__display_cubes(color)
            self.__time_next = 0
        self.__update_cubes(delta)

    def __display_cubes(self, specific_color):
        row = random.randint(0, self.__height // 2)
        col = random.randint(0, self.__width - 1)
        if specific_color != 0:
            color = specific_color
        else:
            color = random.randint(1, 6)
        cube = Cube(self.__screen, col * self.__cube_size, row * self.__cube_size, self.__cube_size, color,
                    (self.__group, self.__cubes_group))
        cube.set_speed(random.randint(250, 450))  # random speed for dynamics
        cube.start_falling(self.__height * self.__cube_size)
        self.__cubes.append(cube)

    def __update_cubes(self, delta):
        for cube in self.__cubes.copy():
            cube.fall(delta)
            cube.draw()

            if cube.is_off_screen():
                cube.kill()
                self.__cubes.remove(cube)

    def clear(self):
        if len(self.__cubes) != 0:
            self.__cubes = [cube.kill() for cube in self.__cubes]
            self.__cubes.clear()

    def __draw_cubes(self):
        for cube in self.__cubes:
            cube.draw()
