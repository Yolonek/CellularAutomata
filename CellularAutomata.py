import numpy as np
from matplotlib.colors import LinearSegmentedColormap


class CellularAutomata:
    def __init__(self, L: int = 30, boundary_conditions: str = 'periodic', rule: int = 30):
        self.L = L
        self.boundary_conditions = boundary_conditions
        self._step = 0
        self.grid = np.zeros(self.L, dtype=np.int8)[None, :]
        self.rule = rule
        self.cases = self.prepare_cases(rule)

    def get_grid(self):
        return self.grid

    @staticmethod
    def convert_number_to_list(number: int, fill_to: int = 3) -> list[int]:
        return [int(digit) for digit in bin(number)[2:].zfill(fill_to)]

    def prepare_cases(self, rule: int) -> dict:
        cases = {}
        rule_in_binary = self.convert_number_to_list(rule, fill_to=8)
        for i in range(7, -1, -1):
            cases[tuple(self.convert_number_to_list(i, fill_to=3))] = True if rule_in_binary[::-1][i] == 1 else False
        return cases

    def change_rule(self, rule: int) -> None:
        self.rule = rule
        self.cases = self.prepare_cases(rule)

    def change_boundary_conditions(self, boundary_conditions: str):
        self.boundary_conditions = boundary_conditions

    def change_grid_size(self, L: int) -> None:
        if self._step == 0:
            self.L = L
            self.grid = np.zeros(self.L, dtype=np.int8)[None, :]
        else:
            raise ValueError(f'Ongoing simulation. Use reset_simulation() first.')

    def reset_simulation(self) -> None:
        self._step = 0
        self.grid = np.zeros(self.L, dtype=np.int8)[None, :]

    def initialize_simulation(self, random: bool = False) -> None:
        if random:
            self.grid[0] = np.random.choice([0, 1], size=self.L).astype(np.int8)
        else:
            self.grid[0, self.L // 2] = 1

    def check_boundary_values(self, array):
        if self.boundary_conditions == 'periodic':
            proximity_left = (array[-1], array[0], array[1])
            proximity_right = (array[-2], array[-1], array[0])
        elif self.boundary_conditions == 'reflective':
            proximity_left = (array[1], array[0], array[1])
            proximity_right = (array[-2], array[-1], array[-2])
        elif self.boundary_conditions == 'constant':
            proximity_left = (1, array[0], array[1])
            proximity_right = (array[-2], array[-1], 1)
        elif self.boundary_conditions == 'null':
            proximity_left = (0, array[0], array[1])
            proximity_right = (array[-2], array[-1], 0)
        elif self.boundary_conditions == 'opposite':
            proximity_left = (0, array[0], array[1])
            proximity_right = (array[-2], array[-1], 1)
        else:
            raise ValueError('Invalid boundary conditions.')
        return proximity_left, proximity_right

    def simulation_step(self) -> None:
        new_generation = np.zeros(self.L, dtype=np.int8)
        current_generation = self.grid[self._step]
        for cell, cell_index in zip(current_generation[1:-1], range(1, self.L - 1)):
            proximity = (current_generation[cell_index - 1], cell, current_generation[cell_index + 1])
            if self.cases[proximity]:
                new_generation[cell_index] = 1

        proximity_left, proximity_right = self.check_boundary_values(current_generation)
        if self.cases[proximity_left]:
            new_generation[0] = 1
        if self.cases[proximity_right]:
            new_generation[-1] = 1

        self.grid = np.concatenate((self.grid, new_generation[None, :]), axis=0)
        self._step += 1

    def simulation(self, steps: int) -> None:
        for _ in range(steps):
            self.simulation_step()

    def plot_grid(self, axes, add_title=False):
        colors = ['#000000', '#ffc130']
        cmap = LinearSegmentedColormap.from_list('', colors, N=len(colors))
        axes.imshow(self.grid, vmin=0, vmax=1, cmap=cmap)
        axes.set(xticks=[], yticks=[])
        if add_title:
            title = (f'Cellular Automata for rule {self.rule}\n'
                     f'Evolution for {self._step} steps, L = {self.L}')
            axes.set_title(title)


if __name__ == '__main__':
    cellular_automata = CellularAutomata(L=20, rule=30)
    cellular_automata.initialize_simulation(random=False)
    cellular_automata.simulation(50)
    print(cellular_automata.grid)
