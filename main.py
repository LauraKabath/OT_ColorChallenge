import pygame as pg
import sys

pg.init()
WIDTH = 800
HEIGHT = 500

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Color Challenge")
clock = pg.time.Clock()

game_font = pg.font.Font("freesansbold.ttf", 30)

while True:
    screen.fill((255, 255, 255))
    x,y = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(60)
