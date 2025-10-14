import copy
import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    """class GameOfLife"""

    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """creating a grid"""
        return [[random.choice([0, int(randomize)]) for col in range(self.cols)] for row in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        """get neighbours"""
        row, col = cell[0], cell[1]
        neighbours = []
        for x, r in enumerate(self.curr_generation):
            for y, _ in enumerate(r):
                if (x == row and abs(col - y) == 1) + (y == col and abs(x - row) == 1) + (
                    abs(row - x) == abs(col - y) and abs(row - x) == 1 and abs(col - y) == 1
                ) == 1:
                    neighbours.append(self.curr_generation[x][y])
        return neighbours

    def get_next_generation(self) -> Grid:
        """getting next generation"""
        grid = copy.deepcopy(self.curr_generation)
        for x, r in enumerate(self.curr_generation):
            for y, c in enumerate(r):
                neighbours = sum(self.get_neighbours((x, y)))
                if (neighbours < 2 or neighbours > 3) and c == 1:
                    grid[x][y] = 0
                if neighbours == 3 and c == 0:
                    grid[x][y] = 1
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation = self.curr_generation
            self.generations += 1
            self.curr_generation = self.get_next_generation()

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        return self.generations >= self.max_generations if self.max_generations else False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> list[list[int]]:
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r", encoding="utf-8") as f:
            grid = [[int(x) for x in line.strip()] for line in f]
        life = GameOfLife((len(grid), len(grid[0])))
        life.curr_generation = grid
        return life.curr_generation

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w", encoding="utf-8") as f:
            for x in self.curr_generation:
                f.write("".join(map(str, x)) + "\n")
