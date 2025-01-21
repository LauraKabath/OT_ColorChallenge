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
        # hover effect for button
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

    # setters for changing button's colors

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
        self.__affected_color = 0
        self.__used = False
        self.deactivate()
        self.set_default_colors()

    def change_color(self):
        # activates button and changes its color
        # so the player knows which color will be affected after clicking on the button
        self.activate()
        self.set_all_colors(COLORS[self.__affected_color], HIGHLIGHT_COLORS[self.__affected_color],
                            BORDER_COLORS[self.__affected_color])

    def set_default_colors(self):
        self.deactivate()
        self.set_all_colors(TAUPE_GRAY, SILVER_GRAY, BLACK)

    def get_color(self):
        return self.__affected_color

    def set_affected_color(self, color_array, condition):
        if condition:
            color_num = self.__find_max(color_array)
        else:
            color_num = self.__find_min(color_array)
        self.__affected_color = color_num
        self.change_color()

    def __find_max(self, color_array):
        maxi_value = color_array[0]
        index = 1
        for i in range(len(color_array)):
            if color_array[i] > maxi_value:
                maxi_value = color_array[i]
                index = i + 1
        return index

    def __find_min(self, color_array):
        if max(color_array) == 0:
            return 1
        else:
            min_value = 10
            index = 0
            for i in range(len(color_array)):
                if color_array[i] < min_value and color_array[i] != 0:
                    min_value = color_array[i]
                    index = i + 1
            return index

    def used(self):
        return self.__used

    def mark_used(self):
        self.__used = True

    def reset(self):
        self.__affected_color = 0
        self.set_default_colors()
        self.__used = False
