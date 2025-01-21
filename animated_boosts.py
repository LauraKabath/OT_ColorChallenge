from colors import *


class Thunder(pg.sprite.Sprite):
    def __init__(self, screen, position, color, groups, size=50):
        super().__init__(groups)
        self.__screen = screen
        self.__position = position
        self.__size = (size, size)
        self.__color = color
        self.__str_color = self.__get_str_color()
        self.__images = []
        self.__get_images()
        self.__state = 0  # index of current image
        self.__life = 1100  # length of life
        self.__A_speed = 500  # animation speed
        self.__time = pg.time.get_ticks()  # spawn time

    def __get_images(self):
        for i in range(1, 4):
            self.__images.append(pg.transform.scale(
                pg.image.load(join('assets', 'images', 'thunder', self.__str_color,
                                   self.__str_color + 'blast' + str(i) + '.png')).convert_alpha(),
                self.__size))

    def __get_str_color(self):
        if self.__color == 1:
            return 'yellow'
        elif self.__color == 2:
            return 'red'
        elif self.__color == 3:
            return 'green'
        elif self.__color == 4:
            return 'blue'
        elif self.__color == 5:
            return 'purple'
        else:
            return 'orange'

    def draw_thunder(self, delta):
        self.__change_state(delta)
        self.__screen.blit(self.__images[self.__state], self.__position)

    def __change_state(self, delta):
        self.__state = int((self.__state + self.__A_speed * delta)) % len(self.__images)

    def disappear(self):
        if pg.time.get_ticks() - self.__time >= self.__life:
            self.kill()
            return True
        return False

    def get_state(self):
        return self.__state

    def get_position(self):
        return self.__position

    def get_color(self):
        return self.__color
