import pygame as pg
import sys

from grid import Grid

pg.init()
WIDTH = 800
HEIGHT = 500

CELL_SIZE = 50
GRID_SIZE = 10


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Color Challenge")
clock = pg.time.Clock()

game = Grid(screen, GRID_SIZE, CELL_SIZE)

game_font = pg.font.Font("freesansbold.ttf", 30)

while True:
    screen.fill((255, 255, 255))
    game.draw_grid()
    x,y = pg.mouse.get_pos()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    pg.display.update()
    clock.tick(60)
