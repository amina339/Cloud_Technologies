"""some imports"""

import copy
import random
import sys
import typing as tp
from turtledemo.sorting_animate import randomize

import pygame

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """class of the game"""

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.cell_size = cell_size
        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.screen_size[0] // self.cell_size
        self.cell_height = self.screen_size[1] // self.cell_size

        # Скорость протекания игры
        self.speed = speed
        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.screen_size[0], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.screen_size[1]))
        for y in range(0, self.screen_size[1], self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.screen_size[0], y))

    def run(self) -> None:
        """Запустить игру"""
        # pylint: disable=no-member
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()


            # Выполнение одного шага игры (обновление состояния ячеек)
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
        sys.exit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        return [
            [random.choice([0, int(randomize)]) for col in range(self.cell_width)] for row in range(self.cell_height)
        ]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        grid = self.grid
        for x in range(1, self.screen_size[1] + 1, self.cell_size):
            for y in range(1, self.screen_size[0] + 1, self.cell_size):
                xpos, ypos = x // self.cell_size, y // self.cell_size
                if grid[xpos][ypos] == 0:
                    pygame.draw.rect(self.screen, pygame.Color("white"), (y, x, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color("green"), (y, x, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: Cell) -> list[int]:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell[0], cell[1]
        neighbours = []
        for x, r in enumerate(self.grid):
            for y, _ in enumerate(r):
                if (x == row and abs(col - y) == 1) + (y == col and abs(x - row) == 1) + (
                    abs(row - x) == abs(col - y) and abs(row - x) == 1 and abs(col - y) == 1
                ) == 1:
                    neighbours.append(self.grid[x][y])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid = copy.deepcopy(self.grid)
        for x, r in enumerate(self.grid):
            for y, c in enumerate(r):
                neighbours = sum(self.get_neighbours((x, y)))
                if (neighbours < 2 or neighbours > 3) and c == 1:
                    grid[x][y] = 0
                if neighbours == 3 and c == 0:
                    grid[x][y] = 1
        return grid


if __name__ == "__main__":
    game = GameOfLife()
    game.run()
