"""some imports"""

from collections.abc import Hashable

import pygame
import pygame.locals

from life import GameOfLife
from ui import UI


class GUI(UI):
    """class GUI"""

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 2) -> None:
        super().__init__(life)
        self.cell_size = cell_size

        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size

        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)
        self.grid = self.life.create_grid(randomize=True)

        self.speed = speed

    def draw_lines(self) -> None:
        # Copy from previous assignment
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        """Отрисовка списка клеток с закрашиванием их в соответствующе цвета."""
        for x in range(1, self.height + 1, self.cell_size):
            for y in range(1, self.width + 1, self.cell_size):
                xpos, ypos = x // self.cell_size, y // self.cell_size
                if self.life.curr_generation[xpos][ypos] == 0:
                    pygame.draw.rect(self.screen, pygame.Color("white"), (y, x, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("green"), (y, x, self.cell_size, self.cell_size))

    def run(self) -> None:
        """Запустить игру"""
        # pylint: disable=no-member
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        font = pygame.font.SysFont("Arial", 35, Hashable)

        self.life.curr_generation = self.life.create_grid(randomize=True)

        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = not pause
                elif event.type == pygame.MOUSEBUTTONDOWN and pause:
                    x, y = pygame.mouse.get_pos()
                    posx = x // self.cell_size
                    posy = y // self.cell_size
                    self.life.curr_generation[posy][posx] = not self.life.curr_generation[posy][posx]
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
            if not pause and not self.life.is_max_generations_exceeded and self.life.is_changing:
                self.life.step()
                self.draw_grid()
                self.draw_lines()
                pygame.display.flip()
            elif self.life.is_max_generations_exceeded or not self.life.is_changing:
                text = font.render("GAME OVER", True, "red")
                rect = text.get_rect()
                rect.center = (self.width // 2, self.height // 2)
                self.screen.fill((0, 0, 0))
                self.screen.blit(text, rect)
                pygame.display.flip()
            elif pause:
                continue
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    live = GameOfLife((50, 50), max_generations=50)
    game = GUI(live)
    game.run()
