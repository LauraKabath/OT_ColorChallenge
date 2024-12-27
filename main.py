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
black = (0, 0, 0)
game = Grid(screen, GRID_SIZE, CELL_SIZE)

game_font = pg.font.Font("freesansbold.ttf", 30)

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = pg.mouse.get_pos()
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                if 0 <= x < game.get_full_size() and 0 <= y < game.get_full_size():
                    if game.get_cell(row, col) != 0:
                        if (row, col) in game.get_selection():
                            game.remove_blocks()
                        else:
                            game.clear_selection()
                            game.select_block(row, col, game.get_cell(row, col))

    screen.fill((255, 255, 255))
    game.draw_grid()
    game.highlight_selection()
    remaining_cells = game_font.render(f"Remaining: {game.get_remaining_cells()}", False, black)
    screen.blit(remaining_cells, (520, 250))
    selected_cells = game_font.render(f"Selected: {len(game.get_selection())}", False, black)
    screen.blit(selected_cells, (520, 220))
    pg.display.update()
    clock.tick(60)
