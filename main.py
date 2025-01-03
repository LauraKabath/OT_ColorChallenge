import sys
import random

from colors import *
from grid import Grid
from text import Text
from button import Button, ColorButton
from boost import Boost
from player import Player

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
        self.__alignment = 590
        self.__score = 0

        self.__score_lbl = Text(self.__screen, self.__alignment, 50, "Score", str(self.__score))
        self.__remaining_cells = Text(self.__screen, self.__alignment - 70, 250, "Remaining",
                                      str(self.__grid.get_remaining_cells()))
        self.__selected_cells = Text(self.__screen, self.__alignment + 70, 250, "Selected",
                                     str(self.__grid.get_selection_count()))

        self.__reset_btn = Button(self.__screen, "RESET", self.__alignment, 320, 120, 40)
        self.__reset_btn.set_all_colors(ROYAL_ORANGE, MAC_N_CHEESE, BRIGHT_RUSSET)
        self.__next_btn = Button(self.__screen, "NEXT LEVEL", self.__alignment - 10, 320, 140, 40)
        self.__end_btn = Button(self.__screen, "FINISH", self.__alignment, 320, 120, 40)
        self.__color_btn = ColorButton(self.__screen, "DELETE", self.__alignment, 380, 120, 40)
        self.__quit_btn = Button(self.__screen, "QUIT", self.__alignment, 440, 120, 40)

        self.__boosts = [Boost(self.__screen, (730, 340)), Boost(self.__screen, (730, 400))]
        self.__activated_boost = False

        self.__player = Player(self.__screen)
        self.__level_lbl = Text(self.__screen, self.__alignment, 150, "Level", str(self.__player.get_level()))

    def __update_game(self):
        self.__screen.fill(MX_BLUE_GREEN)
        self.__grid.draw_grid()
        self.__grid.highlight_selection()

        self.__score_lbl.draw(str(self.__score))
        self.__level_lbl.draw(str(self.__player.get_level()))
        self.__remaining_cells.draw(str(self.__grid.get_remaining_cells()))
        self.__selected_cells.draw(str(self.__grid.get_selection_count()))

        self.__reset_btn.draw_btn()
        self.__quit_btn.draw_btn()
        self.__color_btn.draw_btn()

        self.__reset_btn.deactivate()
        self.__next_btn.deactivate()
        self.__end_btn.deactivate()

        if self.__grid.get_remaining_cells() != 0:
            self.__reset_btn.activate()
            self.__reset_btn.draw_btn()
        else:
            if self.__player.end_level():
                self.__next_btn.activate()
                self.__next_btn.draw_btn()
            else:
                self.__end_btn.activate()
                self.__end_btn.draw_btn()

        for i in range(len(self.__boosts)):
            self.__boosts[i].draw_boost()

    def __calculate_score(self, count, used_boost):
        if used_boost == 0:
            if count < 10:
                self.__score += 15 * count
            elif 10 <= count <= 29:
                self.__score += 20 * count + 10
            elif count >= 30:
                self.__score += 30 * count + 20
        elif used_boost == 1:
            self.__score += count
        elif used_boost == 2:
            self.__score += 2 * count

    def __reset_level(self):
        self.__grid.regenerate()
        self.__color_btn.reset()
        self.__reset_boost()
        self.__score = 0
        self.__activated_boost = False

    def __show_new_level(self):
        self.__player.add_score(self.__score)
        self.__reset_level()

    def __have_boost(self):
        for i in range(len(self.__boosts)):
            if self.__boosts[i].get_state():
                return True
        return False

    def __deactivate_boost(self):
        for i in range(len(self.__boosts)):
            if self.__boosts[i].get_state():
                self.__boosts[i].change_state()
                return

    def __reset_boost(self):
        for i in range(len(self.__boosts)):
            if not self.__boosts[i].get_state():
                self.__boosts[i].change_state()

    def __draw_menu_background(self):
        self.__screen.fill(MX_BLUE_GREEN)
        for row in range(WIDTH):
            for col in range(HEIGHT):
                if random.random() > 0.7:
                    color = COLORS[random.randint(1, 4)]
                    pg.draw.rect(self.__screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    pg.draw.rect(self.__screen, BLACK, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def start_menu(self):
        start_button = Button(self.__screen, "START", WIDTH/2 - 50, HEIGHT/2 + 50, 120, 40)
        title = Text(self.__screen, WIDTH/2 - 50, 140, "Color", "Challenge", 150)
        title.set_color(WHITE)
        start = True
        self.__draw_menu_background()

        while start:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    start = False
                    self.__running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if start_button.is_clicked(event.pos):
                            start = False
                            self.__running = True
                            self.run()

                title.draw_text()
                start_button.draw_btn()
                pg.display.update()
                self.__clock.tick(60)

    def __exit_menu(self):
        self.__draw_menu_background()
        self.__player.show_scores()
        end = True
        while end:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    end = False
            pg.display.update()
            self.__clock.tick(60)
        pg.quit()
        sys.exit()

    def run(self):
        while self.__running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN:
                    x, y = pg.mouse.get_pos()
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if event.button == 1:
                        if 0 <= x < self.__grid.get_full_size() and 0 <= y < self.__grid.get_full_size() and not self.__activated_boost:
                            if self.__grid.get_cell(row, col) != 0:
                                if (row, col) in self.__grid.get_selection():
                                    self.__calculate_score(self.__grid.get_selection_count(), 0)
                                    self.__grid.remove_blocks()
                                else:
                                    self.__grid.clear_selection()
                                    self.__grid.select_block(row, col, self.__grid.get_cell(row, col))
                        else:
                            if self.__reset_btn.is_clicked(event.pos):
                                self.__reset_level()

                            if self.__next_btn.is_clicked(event.pos):
                                self.__show_new_level()

                            if self.__end_btn.is_clicked(event.pos) or self.__quit_btn.is_clicked(event.pos):
                                self.__running = False
                                self.__player.add_score(self.__score)
                                self.__exit_menu()

                            if self.__color_btn.is_clicked(event.pos):
                                count = self.__grid.remove_color(self.__color_btn.get_randomness())
                                self.__calculate_score(count, 1)
                                self.__color_btn.set_default_colors()
                    elif event.button == 3:
                        if 0 <= x < self.__grid.get_full_size() and 0 <= y < self.__grid.get_full_size() and self.__have_boost():
                            if self.__grid.get_cell(row, col) != 0:
                                if (row, col) in self.__grid.get_selection() and self.__activated_boost:
                                    self.__calculate_score(self.__grid.get_selection_count(), 2)
                                    self.__grid.remove_blocks()
                                    self.__deactivate_boost()
                                    self.__activated_boost = False
                                else:
                                    self.__grid.boost_selection(row, col)
                                    self.__activated_boost = True

            if self.__grid.get_remaining_cells() < 50 and not self.__color_btn.is_active():
                self.__color_btn.change_color()

            self.__update_game()
            pg.display.update()
            self.__clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.start_menu()
