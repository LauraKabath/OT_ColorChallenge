import pygame as pg
import sys

from grid import Grid

pg.init()
WIDTH = 800
HEIGHT = 500

CELL_SIZE = 50
CELL_COUNT = 10


screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Color Challenge")
clock = pg.time.Clock()

game = Grid(screen, CELL_COUNT, CELL_SIZE)

game_font = pg.font.Font("freesansbold.ttf", 30)

while True:
    screen.fill((255, 255, 255))
    game.draw_grid()
    game.highlight_selection()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pg.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= x < game.get_size() and 0 <= y < game.get_size():
                    if game.get_cell(row, col) != 0:
                        if (row, col) in game.get_selection():
                            game.remove_blocks()
                        else:
                            game.clear_selection()
                            game.select_block(row, col, game.get_cell(row, col))

    pg.display.update()
    clock.tick(60)
