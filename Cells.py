import pygame
import numpy as np
import numba as nb
from numba.core.errors import NumbaPendingDeprecationWarning
import warnings
warnings.simplefilter('ignore', category=NumbaPendingDeprecationWarning)


class Cells:
    def __init__(self, window, width, height, cell_size):
        self.window = window
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width / cell_size
        self.grid_height = height / cell_size
        self.grid_count = self.grid_width * self.grid_height
        self.cells = set()

    def get_number_of_cells(self) -> int:
        return len(self.cells)

    def clear_cells(self):
        self.cells = set()

    def add_cell(self, cell: tuple[int, int]) -> None:
        x = cell[0] // self.cell_size
        y = cell[1] // self.cell_size
        self.cells.add((x, y))

    def remove_cell(self, cell: tuple[int, int]) -> None:
        x = cell[0] // self.cell_size
        y = cell[1] // self.cell_size
        self.cells.remove((x, y))

    def draw_cells(self, cell_color: tuple[int, int, int]):
        for column, row in self.cells:
            grid_top_left = (column * self.cell_size, row * self.cell_size)
            pygame.draw.rect(self.window, cell_color, (*grid_top_left, self.cell_size, self.cell_size))

    def new_generation(self):
        self.cells = evolve_grid(self.cells, self.width, self.height)

    def generate_random_cells(self):
        occupied_cells = np.random.randint(self.grid_count // 10, self.grid_count // 5)
        self.cells = set(
            [(x, y) for x, y in zip(
                np.random.randint(0, self.grid_width, size=occupied_cells),
                np.random.randint(0, self.grid_height, size=occupied_cells)
            )]
        )


@nb.njit()
def get_all_neighbors(position: tuple[int, int], grid_width: int, grid_height: int) -> list[tuple[int, int]]:
    x, y = position
    neighbors: list[tuple[int, int]] = []
    for dx in [-1, 0, 1]:
        if x + dx < 0 or x + dx > grid_width:
            continue
        for dy in [-1, 0, 1]:
            if y + dy < 0 or y + dy > grid_height:
                continue
            if dx == 0 and dy == 0:
                continue
            neighbors.append((x + dx, y + dy))
    return neighbors


@nb.njit()
def evolve_grid(positions: set[tuple[int, int]], grid_width: int, grid_height: int) -> set[tuple[int, int]]:
    _val = -1
    all_neighbors: set[tuple[int, int]] = {(_val, _val)}
    new_positions: set[tuple[int, int]] = {(_val, _val)}

    for position in positions:
        neighbors = get_all_neighbors(position, grid_width, grid_height)
        all_neighbors.update(neighbors)
        # neighbors = list(filter(lambda x: x in positions, neighbors))
        neighbors = [pos for pos in neighbors if pos in positions]
        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    for position in all_neighbors:
        neighbors = get_all_neighbors(position, grid_width, grid_height)
        # neighbors = list(filter(lambda x: x in positions, neighbors))
        neighbors = [pos for pos in neighbors if pos in positions]
        if len(neighbors) == 3:
            new_positions.add(position)

    all_neighbors.remove((_val, _val))
    new_positions.remove((_val, _val))
    return new_positions


if __name__ == "__main__":
    print(get_all_neighbors((2, 4), 10, 10))
    print(evolve_grid({(2, 2), (5, 5)}, 10, 10))
