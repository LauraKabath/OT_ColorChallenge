from colors import *
from text import Text


class Player:
    def __init__(self, screen):
        self.__screen = screen
        self.__scores = list()
        self.__level = 1
        self.__maxLevel = 12

    def add_score(self, score):
        self.__scores.append(score)
        self.__level += 1

    def get_max_score(self):
        return max(self.__scores)

    def get_min_score(self):
        return min(self.__scores)

    def get_sum_scores(self):
        return sum(self.__scores)

    def get_level(self):
        return self.__level

    def get_mx_level(self):
        return self.__maxLevel

    def end_level(self):
        return self.__level < self.__maxLevel

    def __add_unfinished_levels(self):
        while len(self.__scores) < self.__maxLevel:
            self.__scores.append(0)

    def show_scores(self):
        if self.__level < self.__maxLevel:
            self.__add_unfinished_levels()
        scoreboard = Text(self.__screen, self.__screen.get_width() / 2 - 50, 0, "", "Your Scoreboard", 120)
        scoreboard.set_color(WHITE)
        scoreboard.draw_text()

        for i in range(len(self.__scores)):
            if i < 4:
                score_text = Text(self.__screen, 70, 150 + i * 100, "Level " + str(i + 1), str(self.__scores[i]))
            elif 4 <= i <= 7:
                score_text = Text(self.__screen, 270, 150 + (i - 4) * 100, "Level " + str(i + 1), str(self.__scores[i]))

            else:
                score_text = Text(self.__screen, 470, 150 + (i - 8) * 100, "Level " + str(i + 1), str(self.__scores[i]))
            score_text.draw(str(self.__scores[i]))
        highscore = Text(self.__screen, 670, 250, "Highscore", str(self.get_max_score()))
        lowest_score = Text(self.__screen, 670, 350, "Lowest Score", str(self.get_min_score()))
        highscore.draw(str(self.get_max_score()))
        lowest_score.draw(str(self.get_min_score()))

        total_score = Text(self.__screen, self.__screen.get_width() / 2 - 50, 500, "",
                           "Your final score is " + str(self.get_sum_scores()), 100)
        total_score.set_color(WHITE)
        total_score.draw_text()
