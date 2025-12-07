"""
https://adventofcode.com/2025/day/6
"""
import pathlib
from time import time
import math


def strip_lines(lines_list: list[str]) -> list[str]:
    stripped_lines_list = []
    for item in lines_list:
        stripped_lines_list.append(item.strip())
    return stripped_lines_list


def split_lines(lines_list: list[str], split_on: str | None = None) -> list[str]:
    split_lines_list = []
    for item in lines_list:
        split_lines_list.append(item.split(split_on))
    return split_lines_list


def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')
    # input_file = input_dir.joinpath('sample_input.txt')

    # read input file
    with open(input_file, 'r') as f:
        lines_list = f.readlines()

    # strip each item in data_list
    stripped_lines_list = strip_lines(lines_list)

    # split each line
    split_lines_list = split_lines(stripped_lines_list)

    # last line contains the operators
    operator_row_index = len(split_lines_list) - 1

    total = 0
    for col in range(len(split_lines_list[0])):
        operator = split_lines_list[operator_row_index][col]
        values = []
        for row in range(operator_row_index):
            values.append(int(split_lines_list[row][col]))
        if operator == '+':
            answer = sum(values)
        elif operator == '*':
            answer = math.prod(values)
        else:
            raise ValueError(f'Unknown operator: {operator}')

        total += answer

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {total}')


if __name__ == "__main__":
    main()
