"""
https://adventofcode.com/2025/day/4
"""
import pathlib
from time import time

ADJACENT_COMBINATIONS = [
    (1, 0),
    (1, 1),
    (0, 1),
    (-1, 1),
    (-1, 0),
    (0, -1),
    (1, -1),
    (-1, -1),
]


class Cell:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y


class Grid:
    def __init__(self):
        self.grid = []

    def add_row(self, row: list):
        self.grid.append(row)

    def _count_adjacent_cells(self, x, y, search_value) -> int:
        count = 0
        for x_adjustment, y_adjustment in ADJACENT_COMBINATIONS:
            x_search = x + x_adjustment
            y_search = y + y_adjustment
            # check x and y are within grid
            if 0 <= x_search < len(self.grid[0]) and 0 <= y_search < len(self.grid):
                # check if cell value matches search value
                if self.grid[y_search][x_search].value == search_value:
                    count += 1
        return count

    def count_accessible_cells(self, limit: int) -> int:
        counter = 0
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell.value == '@':
                    num_adjacent_cells = self._count_adjacent_cells(x=x,
                                                                   y=y,
                                                                   search_value='@')
                    if num_adjacent_cells < limit:
                        counter += 1
                        # remove paper roll
                        self.grid[y][x].value = 'x'
        return counter


def main(limit: int):
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')
    # input_file = input_dir.joinpath('sample_input.txt')

    # read input file
    with open(input_file, 'r') as f:
        rows_list = f.readlines()

    # create a list of lists to describe the grid
    # top left corner is 0,0
    # x horizontal, y vertical
    grid = Grid()
    for y, row in enumerate(rows_list):
        cell_list = []
        row = row.strip()
        for x, cell in enumerate(row):
            cell_list.append(Cell(value=cell, x=x, y=y))
        grid.add_row(cell_list)

    counter = 0
    # count and remove paper rolls until no more are possible
    while True:
        total = grid.count_accessible_cells(limit=limit)
        counter += total
        if total == 0:
            break

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {counter}')


if __name__ == "__main__":
    main(limit=4)