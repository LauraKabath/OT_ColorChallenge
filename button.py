import random

from colors import *


class Button:
    def __init__(self, screen, name, x, y, width, height):
        self.__screen = screen
        self.__name = name
        self._active = True
        self.__font = pg.font.Font(join('assets', 'fonts', 'AvenuePixel-Regular.ttf'), height)
        self.__shape = pg.Rect(x, y, width, height)
        self.__color = CRAYOLA_GOLD
        self.__hoverColor = WHITE_CHOCOLATE
        self.__txtColor = COPPER
        self.__text = self.__font.render(self.__name, True, self.__txtColor)
        self.__txtRect = self.__text.get_rect(centerx=x + width / 2, centery=y + height / 2)

    def draw_btn(self):
        px, py = pg.mouse.get_pos()
        if self.__shape.x <= px <= self.__shape.x + self.__shape.width and self.__shape.y <= py <= self.__shape.y + self.__shape.height:
            pg.draw.rect(self.__screen, self.__hoverColor, self.__shape, border_radius=15)
        else:
            pg.draw.rect(self.__screen, self.__color, self.__shape, border_radius=15)

        pg.draw.rect(self.__screen, self.__txtColor, self.__shape, width=2, border_radius=15)
        self.__screen.blit(self.__text, self.__txtRect)

    def is_clicked(self, pos):
        if self._active:
            return self.__shape.collidepoint(pos)
        return False

    def is_active(self):
        return self._active

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def __render_txt(self):
        self.__text = self.__font.render(self.__name, True, self.__txtColor)

    def set_btn_color(self, new_color):
        self.__color = new_color

    def set_hover_color(self, new_hover_color):
        self.__hoverColor = new_hover_color

    def set_txt_color(self, new_txt_color):
        self.__txtColor = new_txt_color
        self.__render_txt()

    def set_all_colors(self, new_color, new_hover_color, new_txt_color):
        self.set_btn_color(new_color)
        self.set_hover_color(new_hover_color)
        self.set_txt_color(new_txt_color)


class ColorButton(Button):
    def __init__(self, screen, name, x, y, width, height):
        super().__init__(screen, name, x, y, width, height)
        self.__randomness = random.randint(1, 4)
        self.deactivate()
        self.set_default_colors()

    def change_color(self):
        self.activate()
        self.set_all_colors(COLORS[self.__randomness], HIGHLIGHT_COLORS[self.__randomness],
                            BORDER_COLORS[self.__randomness])

    def set_default_colors(self):
        self.set_all_colors(TAUPE_GRAY, SILVER_GRAY, BLACK)

    def get_randomness(self):
        return self.__randomness

    def reset(self):
        self.__randomness = random.randint(1, 4)
        self.deactivate()
        self.set_default_colors()
