"""
https://adventofcode.com/2025/day/9
"""
import pathlib
from time import time
import math


class Rectangle:
    def __init__(self, corner1, corner2):
        self.corner1 = corner1
        self.corner2 = corner2
        self._calculate_length_and_width()
        self._calculate_area()

    def _calculate_length_and_width(self):
        x1, y1 = self.corner1.split(',')
        x2, y2 = self.corner2.split(',')

        self.length = abs(int(x1) - int(x2)) + 1
        self.width = abs(int(y1) - int(y2)) + 1

    def _calculate_area(self):
        self.area = self.length * self.width


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
        node_list = f.readlines()

    # strip leading and trailing whitespace
    node_list = strip_lines(node_list)
    number_of_nodes = len(node_list)

    # iterate over every combination of nodes and create list of areas
    areas = []
    while True:
        current_node = node_list.pop()
        for node in node_list:
            rectangle = Rectangle(current_node, node)
            areas.append(rectangle.area)
        if len(node_list) == 0:
            break

    max_area = max(areas)

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Max area: {max_area}')


if __name__ == "__main__":
    main()
