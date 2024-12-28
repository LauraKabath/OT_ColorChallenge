import pygame as pg
import sys

from grid import Grid

WIDTH = 800
HEIGHT = 500

CELL_SIZE = 50
GRID_SIZE = 10
BLACK = (0, 0, 0)


class Game:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Color Challenge")
        self.__clock = pg.time.Clock()
        self.__grid = Grid(self.__screen, GRID_SIZE, CELL_SIZE)
        self.__running = True
        self.__font = pg.font.Font("freesansbold.ttf", 30)
        self.__remaining_cells = self.__font.render(f"Remaining: {self.__grid.get_remaining_cells()}", False, BLACK)
        self.__selected_cells = self.__font.render(f"Selected: {len(self.__grid.get_selection())}", False, BLACK)

    def update(self):
        self.__remaining_cells = self.__font.render(f"Remaining: {self.__grid.get_remaining_cells()}", False, BLACK)
        self.__selected_cells = self.__font.render(f"Selected: {len(self.__grid.get_selection())}", False, BLACK)
        self.__screen.blit(self.__remaining_cells, (520, 250))
        self.__screen.blit(self.__selected_cells, (520, 220))

    def run(self):
        while self.__running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = pg.mouse.get_pos()
                        col = x // CELL_SIZE
                        row = y // CELL_SIZE
                        if 0 <= x < self.__grid.get_full_size() and 0 <= y < self.__grid.get_full_size():
                            if self.__grid.get_cell(row, col) != 0:
                                if (row, col) in self.__grid.get_selection():
                                    self.__grid.remove_blocks()
                                else:
                                    self.__grid.clear_selection()
                                    self.__grid.select_block(row, col, self.__grid.get_cell(row, col))
            self.__screen.fill((255, 255, 255))
            self.__grid.draw_grid()
            self.__grid.highlight_selection()
            self.update()
            pg.display.update()
            self.__clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
