from colors import *


class Text:
    def __init__(self, screen, px, py, lbl, value, font=50):
        self.__screen = screen
        self.__lbl = lbl
        self.__val = value
        self.__color = DARK_GREEN
        self.__font_size = font
        self.__rect = pg.Rect(px, py, 120, font - 10)
        self.__font = pg.font.Font(join('assets', 'fonts', 'AvenuePixelSoft-Stroke-Regular.ttf'), self.__font_size)
        self.__label = self.__font.render(self.__lbl, True, self.__color)
        self.__value = self.__font.render(self.__val, True, self.__color)

    def draw(self, value):
        # draws formatted text and the value in the rectangle
        pg.draw.rect(self.__screen, PALE_BLUE, self.__rect, border_radius=10)
        self.__value = self.__font.render(value, True, self.__color)
        self.__screen.blit(self.__value, self.__value.get_rect(
            centerx=self.__rect.centerx,
            centery=self.__rect.centery))
        self.__screen.blit(self.__label, self.__label.get_rect(
            centerx=self.__rect.centerx,
            centery=self.__rect.centery - self.__rect.height))

    def draw_text(self):
        # draws formatted text and the value without rectangle
        self.__value = self.__font.render(self.__val, True, self.__color)
        self.__screen.blit(self.__value, self.__value.get_rect(
            centerx=self.__rect.centerx,
            centery=self.__rect.centery))
        self.__screen.blit(self.__label, self.__label.get_rect(
            centerx=self.__rect.centerx,
            centery=self.__rect.centery - self.__rect.height))

    def set_color(self, color):
        self.__color = color
        self.__render_txt()

    def set_rect_width(self, width):
        self.__rect.width = width

    def __render_txt(self):
        self.__label = self.__font.render(self.__lbl, True, self.__color)
        self.__value = self.__font.render(self.__val, True, self.__color)
