import sys

from colors import *
from grid import Grid
from text import Text
from button import Button, ColorButton
from boost import Boost
from player import Player
from background import Background

CELL_SIZE = 50
GRID_SIZE = 12
WIDTH = CELL_SIZE * GRID_SIZE + 300
HEIGHT = CELL_SIZE * GRID_SIZE


class Sound(pg.mixer.Sound):
    def __init__(self, filename, volume=0.3):
        super().__init__(join('assets', 'sounds', filename))
        self.set_volume(volume)


class Game:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Color Challenge")
        self.__clock = pg.time.Clock()
        self.__grid = Grid(self.__screen, GRID_SIZE, CELL_SIZE)
        self.__running = True
        self.__alignment = self.__grid.get_full_size() + 90
        self.__score = 0
        # initialisation of text labels
        self.__score_lbl = Text(self.__screen, self.__alignment, 50, "Score", str(self.__score))
        self.__remaining_cells = Text(self.__screen, self.__alignment - 70, 250, "Remaining",
                                      str(self.__grid.get_remaining_cells()))
        self.__selected_cells = Text(self.__screen, self.__alignment + 70, 250, "Selected",
                                     str(self.__grid.get_selection_count()))
        # initialisation of buttons
        self.__reset_btn = Button(self.__screen, "RESET", self.__alignment, 320, 120, 40)
        self.__reset_btn.set_all_colors(PASTEL_PINK, BABY_PINK, CAPPUCCINO)
        self.__next_btn = Button(self.__screen, "NEXT LEVEL", self.__alignment - 10, 320, 140, 40)
        self.__end_btn = Button(self.__screen, "FINISH", self.__alignment, 320, 120, 40)
        self.__color_btn = ColorButton(self.__screen, "DELETE", self.__alignment, 380, 120, 40)
        self.__thunder_btn = ColorButton(self.__screen, "THUNDER", self.__alignment, 440, 120, 40)
        self.__quit_btn = Button(self.__screen, "QUIT", self.__alignment, 500, 120, 40)
        # initialisation of boosts
        self.__boosts = [Boost(self.__screen, (820, 340)), Boost(self.__screen, (820, 400))]
        self.__activated_boost = False
        self.__boost_addition = False
        # initialisation of player
        self.__player = Player(self.__screen)
        self.__level_lbl = Text(self.__screen, self.__alignment, 150, "Level", str(self.__player.get_level()))
        # sounds for the game
        self.__btn_click_sound = Sound('button_pressed.mp3')
        self.__block_collapse_sound = Sound('block_collapse.mp3', 0.2)
        self.__applause_sound = Sound('applause.mp3')
        self.__click_sound = Sound('click1.mp3')
        self.__explosion_sound = Sound('explosion.mp3')
        self.__thunder_sound = Sound('thunder.mp3')
        self.__loud_thunder_sound = Sound('thunder.mp3', 1.5)
        self.__ticking_sound = Sound('ticking.mp3')
        self.__start_sound = Sound('arcade.mp3', 1.7)
        # menu background
        self.__background = Background(self.__screen, CELL_SIZE)

    def __update_game(self, delta):  # updates/redraws all the components in game
        self.__screen.fill(MX_BLUE_GREEN)
        # cubes/grid animation
        self.__grid.fall(delta)
        self.__grid.shift(delta)
        self.__grid.draw_grid(delta)
        # labels
        self.__score_lbl.draw(str(self.__score))
        self.__level_lbl.draw(str(self.__player.get_level()))
        self.__remaining_cells.draw(str(self.__grid.get_remaining_cells()))
        self.__selected_cells.draw(str(self.__grid.get_selection_count()))
        # buttons
        self.__reset_btn.draw_btn()
        self.__quit_btn.draw_btn()
        self.__color_btn.draw_btn()
        self.__thunder_btn.draw_btn()
        # deactivation of buttons
        self.__reset_btn.deactivate()
        self.__next_btn.deactivate()
        self.__end_btn.deactivate()
        # conditions which determines which button to draw according to the block count
        if self.__grid.get_remaining_cells() != 0:  # the grid is not cleared = level is not finished
            self.__reset_btn.activate()
            self.__reset_btn.draw_btn()
        else:  # grid is cleared
            if self.__player.end_level():  # not in the final level
                self.__next_btn.activate()
                self.__next_btn.draw_btn()
            else:  # finished final level
                self.__end_btn.activate()
                self.__end_btn.draw_btn()

        # condition for adding an extra boost to the game
        if self.__player.get_level() == 9 and not self.__boost_addition:
            self.__boosts.append(Boost(self.__screen, (820, 460)))
            self.__boost_addition = True

        for i in range(len(self.__boosts)):
            self.__boosts[i].draw_boost()

    def __calculate_score(self, count, used_boost):
        # calculates score based on count of deleted blocks and condition if boost was used
        if used_boost == 0:  # boost wasn't used
            if count < 10:
                self.__score += 15 * count
            elif 10 <= count <= 29:
                self.__score += 20 * count + 10
            elif count >= 30:
                self.__score += 30 * count + 20
        elif used_boost == 1:  # boost: DELETE color_btn was used
            self.__score += count
        elif used_boost == 2:  # boost: Bomb was used
            self.__score += 2 * count

    def __reset_level(self):
        # resets level after clicking on reset_btn
        self.__grid.regenerate(self.__player.get_level())
        self.__ticking_sound.stop()
        self.__color_btn.reset()
        self.__thunder_btn.reset()
        self.__reset_boost()
        self.__score = 0
        self.__activated_boost = False

    def __show_new_level(self):
        # loads new level after clicking on next_btn
        self.__player.add_score(self.__score)
        self.__reset_level()

    def __have_boost(self):
        # return boolean value if the player / game have boost: bomb
        for i in range(len(self.__boosts)):
            if self.__boosts[i].get_state():
                return True
        return False

    def __deactivate_boost(self):
        # deactivates boost: bomb when used
        for i in range(len(self.__boosts)):
            if self.__boosts[i].get_state():
                self.__boosts[i].change_state()
                return

    def __reset_boost(self):
        # resets boost: bomb for a new level or reset
        for i in range(len(self.__boosts)):
            if not self.__boosts[i].get_state():
                self.__boosts[i].change_state()

    def start_menu(self):
        # displays start screen
        start_button = Button(self.__screen, "START", WIDTH/2 - 50, HEIGHT/2 + 50, 120, 40)
        title = Text(self.__screen, WIDTH/2 - 50, 140, "Color", "Challenge", 150)
        title.set_color(WHITE)
        self.__start_sound.play(loops=-1)
        start = True
        while start:
            delta = self.__clock.tick() / 1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    start = False
                    self.__running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if start_button.is_clicked(event.pos):
                            self.__btn_click_sound.play()
                            start = False
                            self.__running = True
                            self.__start_sound.stop()
                            self.__background.clear()
                            self.run()
            self.__background.draw_animated_background(delta)
            title.draw_text()
            start_button.draw_btn()
            pg.display.update()

    def __exit_menu(self):
        # display exit screen
        self.__applause_sound.play()
        self.__background.draw_frame()
        self.__player.show_scores()  # draws player's scoreboard
        end = True
        while end:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    end = False
            pg.display.update()
            self.__clock.tick()
        pg.quit()
        sys.exit()

    def run(self):
        # main game loop
        while self.__running:
            delta = self.__clock.tick() / 1000
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN and not (self.__grid.get_thunder() or self.__grid.get_explosion()):
                    x, y = pg.mouse.get_pos()
                    col = x // CELL_SIZE
                    row = y // CELL_SIZE
                    if event.button == 1:  # left mouse button: grid blocks
                        if 0 <= x < self.__grid.get_full_size() and 0 <= y < self.__grid.get_full_size() and not self.__activated_boost:
                            if self.__grid.get_cell(row, col) != 0:
                                if (row, col) in self.__grid.get_selection():
                                    self.__block_collapse_sound.play()
                                    self.__calculate_score(self.__grid.get_selection_count(), 0)
                                    self.__grid.remove_blocks()
                                else:
                                    self.__click_sound.play()
                                    self.__grid.clear_selection()
                                    self.__grid.select_block(row, col, self.__grid.get_cell(row, col))
                        else:  # button clicked
                            if self.__reset_btn.is_clicked(event.pos):
                                self.__btn_click_sound.play()
                                self.__reset_level()

                            if self.__next_btn.is_clicked(event.pos):
                                self.__btn_click_sound.play()
                                self.__show_new_level()

                            if self.__end_btn.is_clicked(event.pos) or self.__quit_btn.is_clicked(event.pos):
                                self.__btn_click_sound.play()
                                self.__running = False
                                self.__player.add_score(self.__score)
                                self.__exit_menu()

                            if self.__color_btn.is_clicked(event.pos):
                                self.__btn_click_sound.play()
                                count = self.__grid.remove_color(self.__color_btn.get_color())
                                self.__calculate_score(count, 1)
                                self.__color_btn.set_default_colors()
                                self.__color_btn.mark_used()

                            if self.__thunder_btn.is_clicked(event.pos):
                                near = self.__grid.thunder_charge(self.__thunder_btn.get_color())
                                if near:
                                    self.__loud_thunder_sound.play()
                                else:
                                    self.__thunder_sound.play()
                                self.__thunder_btn.set_default_colors()
                                self.__thunder_btn.mark_used()
                    elif event.button == 3:  # right mouse button: boost bomb
                        if 0 <= x < self.__grid.get_full_size() and 0 <= y < self.__grid.get_full_size() and self.__have_boost():
                            if self.__grid.get_cell(row, col) != 0:
                                if (row, col) in self.__grid.get_selection() and self.__activated_boost:
                                    self.__explosion_sound.play()
                                    self.__ticking_sound.stop()
                                    self.__calculate_score(self.__grid.get_selection_count(), 2)
                                    self.__grid.activate_explosion()
                                    self.__deactivate_boost()
                                    self.__activated_boost = False
                                else:
                                    self.__ticking_sound.play(loops=-1)
                                    self.__grid.boost_selection(row, col)
                                    self.__activated_boost = True
                    elif event.button == 2:  # middle mouse button: deactivate boost: bomb
                        self.__click_sound.play()
                        self.__ticking_sound.stop()
                        self.__activated_boost = False
                        self.__grid.clear_selection()
                        self.__grid.clear_explosion()

            # conditions for color buttons activation
            color_counts = self.__grid.get_color_counts(self.__player.get_level())
            if self.__grid.get_remaining_cells() < 55 and not self.__color_btn.used():
                self.__color_btn.set_affected_color(color_counts, True)

            if self.__grid.get_remaining_cells() < 80 and not self.__thunder_btn.used():
                self.__thunder_btn.set_affected_color(color_counts, False)

            self.__update_game(delta)
            pg.display.update()


if __name__ == "__main__":
    game = Game()
    game.start_menu()
