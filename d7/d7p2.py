"""
https://adventofcode.com/2025/day/7
"""
import pathlib
from time import time


class Cell:
    def __init__(self, value):
        self.value = value
        self.beam_count = 0


class Grid:
    def __init__(self):
        self.grid = []

    def add_row(self, row: list):
        self.grid.append(row)

    def count_splits(self) -> int:
        split_count = 0
        for row_index, row in enumerate(self.grid):
            row_split_count = self._process_row(row_index)
            split_count += row_split_count
        return split_count

    def _process_row(self, row_index: int) -> int:
        row_split_count = 0
        for column_index, cell in enumerate(self.grid[row_index]):
            if cell.value == 'S':
                self.grid[row_index + 1][column_index].value = '|'
                self.grid[row_index + 1][column_index].beam_count += 1
            elif cell.value == '^':
                if self.grid[row_index - 1][column_index].value == '|':
                    input_beam_count = self.grid[row_index - 1][column_index].beam_count
                    # split beam. Assuming ^ can't be beside each other or at edge
                    row_split_count += 1
                    self.grid[row_index][column_index + 1].value = '|'
                    self.grid[row_index][column_index + 1].beam_count += input_beam_count
                    self.grid[row_index][column_index - 1].value = '|'
                    self.grid[row_index][column_index - 1].beam_count += input_beam_count
            else:
                if self.grid[row_index - 1][column_index].value == '|':
                    # continue beam
                    cell.value = '|'
                    cell.beam_count += self.grid[row_index - 1][column_index].beam_count
        return row_split_count

    def count_output_beams(self) -> int:
        output_beam_count = 0
        for cell in self.grid[-1]:
            output_beam_count += cell.beam_count
        return output_beam_count


def strip_lines(lines_list: list[str]) -> list[str]:
    stripped_lines_list = []
    for item in lines_list:
        stripped_lines_list.append(item.strip())
    return stripped_lines_list


def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')
    # input_file = input_dir.joinpath('sample_input.txt')

    # read input file
    with open(input_file, 'r') as f:
        rows_list = f.readlines()

    # strip leading and trailing whitespace
    rows_list = strip_lines(rows_list)

    # create a list of lists to describe the grid
    # top left corner is 0,0
    # x horizontal, y vertical
    grid = Grid()
    for y, row in enumerate(rows_list):
        cell_list = []
        for x, cell in enumerate(row):
            cell_list.append(Cell(value=cell))
        grid.add_row(cell_list)

    split_count = grid.count_splits()
    output_beams = grid.count_output_beams()

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Number of splits: {split_count}')
    print(f'Timelines: {output_beams}')


if __name__ == "__main__":
    main()
