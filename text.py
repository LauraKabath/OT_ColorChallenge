from colors import *


class Text:
    def __init__(self, screen, px, py, lbl, value):
        self.__screen = screen
        self.__color = BLACK
        self.__font_size = 50
        self.__rect_width = 120
        self.__rect_height = 40
        self.__rect = pg.Rect(px, py, self.__rect_width, self.__rect_height)
        self.__font = pg.font.Font(join('assets', 'fonts', 'AvenuePixelSoft-Stroke-Regular.ttf'), self.__font_size)
        self.__label = self.__font.render(lbl, True, self.__color)
        self.__value = self.__font.render(value, True, self.__color)

    def draw(self, value):
        pg.draw.rect(self.__screen, WHITE, self.__rect, border_radius=10)
        self.__value = self.__font.render(value, True, self.__color)
        self.__screen.blit(self.__value, self.__value.get_rect(
            centerx=self.__rect.centerx,
            centery=self.__rect.centery))
        self.__screen.blit(self.__label, self.__label.get_rect(
            centerx=self.__rect.centerx,
            centery=self.__rect.centery - self.__rect_height))

    def set_color(self, color):
        self.__color = color

    def set_font_size(self, size):
        self.__font_size = size

    def set_rect_width(self, width):
        self.__rect_width = width

    def set_rect_height(self, height):
        self.__rect_height = height
