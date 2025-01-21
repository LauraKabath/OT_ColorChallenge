from colors import *


class GroupGrid(pg.sprite.Group):
    def __init__(self):
        super().__init__()


class Cube(pg.sprite.Sprite):
    def __init__(self, screen, x, y, size, color, groups):
        super().__init__(groups)
        self.__screen = screen
        self.__size = size
        self.__x = x
        self.__y = y
        self.__speed = 350
        self.__target_y = y  # falling target
        self.__target_x = x  # shifting target
        self.__color_index = color
        self.__color = COLORS[color]
        self.__highlightColor = HIGHLIGHT_COLORS[color] if color != 0 else SILVER_GRAY
        self.__selected = False
        self.__falling = False  # falling animation indicator
        self.__shifting = False  # shifting animation indicator

    def draw(self):
        rect = pg.Rect(self.__x, self.__y, self.__size, self.__size)
        if self.__selected:
            pg.draw.rect(self.__screen, self.__highlightColor, rect)
        else:
            pg.draw.rect(self.__screen, self.__color, rect)
        if self.__color_index != 0:
            pg.draw.rect(self.__screen, BLACK, rect, 1)

    def select(self):
        self.__selected = True

    def unselect(self):
        self.__selected = False

    def resize(self, size):
        self.__size = size

    def start_falling(self, target_y):
        self.__target_y = target_y
        self.__falling = True

    def fall(self, delta):
        if self.__falling:
            if self.__y < self.__target_y:
                self.__y += self.__speed * delta
                if self.__y >= self.__target_y:
                    self.__y = self.__target_y
                    self.__falling = False
            elif self.__y > self.__target_y:
                self.__y = self.__target_y
                self.__falling = False

    def start_shifting(self, target_x):
        self.__target_x = target_x
        self.__shifting = True

    def shift(self, delta):
        if self.__shifting:
            if self.__x > self.__target_x:
                self.__x -= self.__speed * delta
                if self.__x <= self.__target_x:
                    self.__x = self.__target_x
                    self.__shifting = False
            elif self.__x < self.__target_x:
                self.__x = self.__target_x
                self.__shifting = False

    def change_color(self, color):
        self.__color_index = color
        self.__color = COLORS[color]
        self.__highlightColor = HIGHLIGHT_COLORS[color] if color != 0 else COLORS[color]
