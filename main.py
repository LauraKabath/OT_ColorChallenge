import sys

from colors import *
from grid import Grid
from text import Text

CELL_SIZE = 50
GRID_SIZE = 10
WIDTH = CELL_SIZE * GRID_SIZE + 300
HEIGHT = CELL_SIZE * GRID_SIZE


class Game:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Color Challenge")
        self.__clock = pg.time.Clock()
        self.__grid = Grid(self.__screen, GRID_SIZE, CELL_SIZE)
        self.__running = True
        self.__alignment = 550
        self.__score = 0
        self.__score_lbl = Text(self.__screen, self.__alignment, 50, "Score", str(self.__score))
        self.__remaining_cells = Text(self.__screen, self.__alignment, 150, "Remaining", str(self.__grid.get_remaining_cells()))
        self.__selected_cells = Text(self.__screen, self.__alignment, 250, "Selected", str(len(self.__grid.get_selection())))

    def __update_game(self):
        self.__grid.draw_grid()
        self.__grid.highlight_selection()

        self.__score_lbl.draw(str(self.__score))
        self.__remaining_cells.draw(str(self.__grid.get_remaining_cells()))
        self.__selected_cells.draw(str(len(self.__grid.get_selection())))

    def __calculate_score(self, count):
        if count < 10:
            self.__score += 15 * count
        elif 10 <= count <= 29:
            self.__score += 20 * count + 10
        elif count >= 30:
            self.__score += 30 * count + 20

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
                                    self.__calculate_score(len(self.__grid.get_selection()))
                                    self.__grid.remove_blocks()
                                else:
                                    self.__grid.clear_selection()
                                    self.__grid.select_block(row, col, self.__grid.get_cell(row, col))
            self.__screen.fill(MX_BLUE_GREEN)
            self.__update_game()
            pg.display.update()
            self.__clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
