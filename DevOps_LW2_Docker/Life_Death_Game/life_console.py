"""some imports"""

import curses
import time

from life import GameOfLife
from ui import UI

class Console(UI):
    """class Console"""

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.rows = len(self.life.curr_generation)
        self.cols = len(self.life.curr_generation[0])

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border()

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for i in range(self.rows):
            for j in range(self.cols):
                if self.life.curr_generation[i][j] == 1:
                    screen.addstr(i + 1, j * 2 + 1, "♘")
                else:
                    screen.addstr(i + 1, j * 2 + 1, "♞")
        screen.refresh()

    def run(self):
        screen = curses.initscr()
        curses.curs_set(0)
        screen.nodelay(True)
        sign = True
        pause = False
        while True:
            screen.clear()
            if sign:
                self.draw_borders(screen)
                self.draw_grid(screen)

            if not self.life.is_max_generations_exceeded and self.life.is_changing and not pause:
                self.life.step()
                screen.refresh()
            elif self.life.is_max_generations_exceeded and self.life.is_changing:
                screen.clear()
                screen.addstr(0, 0, "The number of possible generations has exceeded" '\nPlease, press "X" to exit')
                screen.refresh()
                sign = False
            elif not self.life.is_max_generations_exceeded and not self.life.is_changing:
                screen.clear()
                screen.addstr(0, 0, "You have reached the final state of life " '\nPlease, press "X" to exit')
                screen.refresh()
                sign = False
            time.sleep(0.5)
            key = screen.getch()
            if key == ord("X"):
                break
            if key == ord("P"):
                pause = not pause
        curses.endwin()


if __name__ == "__main__":
    game = GameOfLife((30, 30), max_generations=50)
    ui = Console(game)
    ui.run()
