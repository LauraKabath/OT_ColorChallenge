from colors import *


class Boost:
    def __init__(self, screen, position, size=50):
        self.__screen = screen
        self.__state = 1  # 0-used 1-active
        self.__size = (size, size)
        self.__active_img = pg.transform.scale(pg.image.load(join('assets', 'images', 'black.png')).convert_alpha(),
                                               self.__size)
        self.__used_img = pg.transform.scale(pg.image.load(join('assets', 'images', 'white.png')).convert_alpha(),
                                             self.__size)
        self.__images = [self.__used_img, self.__active_img]
        self.__position = position

    def draw_boost(self):
        self.__screen.blit(self.__images[self.__state], self.__position)

    def change_state(self):
        self.__state = not self.__state
        self.draw_boost()

    def get_state(self):
        return self.__state
