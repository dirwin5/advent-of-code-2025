"""
https://adventofcode.com/2025/day/9

Not a great solution but gets there. Took about 20 minutes to run.
"""
import pathlib
from time import time

import numpy as np


class Rectangle:
    def __init__(self,
                 corner1: tuple[int, int],
                 corner2: tuple[int, int]):
        self.corner1 = corner1
        self.corner2 = corner2
        self._calculate_length_and_width()
        self._calculate_area()

    def _calculate_length_and_width(self):
        self.x1, self.y1 = self.corner1
        self.x2, self.y2 = self.corner2

        self.length = abs(self.x1 - self.x2) + 1
        self.width = abs(self.y1 - self.y2) + 1

    def _calculate_area(self):
        self.area = self.length * self.width

    def count_internal_vertices(self, node_list) -> int:
        print(f'Current rectangle: Area: {self.area}, Corner1: {self.corner1}, '
              f'Corner2: {self.corner2}')
        count = 0
        for node in node_list:
            x, y = node
            if min(self.x1, self.x2) < x < max(self.x2, self.x1):
                if min(self.y1, self.y2) < y < max(self.y2, self.y1):
                    count += 1
                    break

        return count

class Polygon:
    def __init__(self, node_list: list[tuple[int, int]]):
        self.node_list = node_list
        self.clockwise = None
        self._check_direction()

    def _check_direction(self):
        previous_direction = None
        direction_count = 0
        first_node = self.node_list[0]
        for i, node in enumerate(self.node_list):
            # wrap to first node at end
            if i == len(self.node_list) - 1:
                next_node = first_node
            else:
                next_node = self.node_list[i + 1]
            direction = self._find_line_direction(node, next_node)
            # direction = self._draw_line(node, next_node)
            if i == 0:
                first_direction = direction
            # track direction changes
            if previous_direction is not None:
                if direction - previous_direction == 1 or direction - previous_direction == -3:
                    # clockwise
                    direction_count += 1
                else:
                    # anti-clockwise
                    direction_count -= 1
            previous_direction = direction

        # check if polygon was clockwise or anti-clockwise
        if direction_count > 0:
            # 1 = clockwise. -1 = anti-clockwise
            self.clockwise = True
        else:
            self.clockwise = False

    @staticmethod
    def _find_line_direction(node: tuple[int, int], next_node: tuple[int, int]) -> int:
        x1, y1 = node
        x2, y2 = next_node
        # up=1, right=2, down=3, left=4
        if x2 > x1:
            return 2
        elif x2 < x1:
            return 4
        elif y2 > y1:
            return 3
        elif y2 < y1:
            return 1
        else:
            raise ValueError("Unexpected direction")

    def buffer_polygon(self) -> 'Polygon':
        buffered_node_list = []
        previous_direction = None
        first_node = self.node_list[0]
        for i, node in enumerate(self.node_list):
            # get next_node
            # wrap to first node at end
            if i == len(self.node_list) - 1:
                next_node = first_node
            else:
                next_node = self.node_list[i + 1]
            # get previous node
            if i == 0:
                previous_node = self.node_list[-1]
            else:
                previous_node = self.node_list[i - 1]
            incoming_direction = self._find_line_direction(previous_node, node)
            outgoing_direction = self._find_line_direction(node, next_node)

            buffered_node = self._find_buffered_node(node, incoming_direction, outgoing_direction)
            buffered_node_list.append(buffered_node)

        buffered_polygon = Polygon(buffered_node_list)
        return buffered_polygon

    def _find_buffered_node(self, node, incoming_direction, outgoing_direction) -> tuple[int, int]:
        # up=1, right=2, down=3, left=4
        if incoming_direction == 1:
            if outgoing_direction == 2:
                if self.clockwise:
                    buffered_node = (node[0] - 1, node[1] - 1)
                else:
                    buffered_node = (node[0] + 1, node[1] + 1)
            elif outgoing_direction == 4:
                if self.clockwise:
                    buffered_node = (node[0] - 1, node[1] + 1)
                else:
                    buffered_node = (node[0] + 1, node[1] - 1)
        elif incoming_direction == 2:
            if outgoing_direction == 3:
                if self.clockwise:
                    buffered_node = (node[0] + 1, node[1] - 1)
                else:
                    buffered_node = (node[0] - 1, node[1] + 1)
            elif outgoing_direction == 1:
                if self.clockwise:
                    buffered_node = (node[0] - 1, node[1] - 1)
                else:
                    buffered_node = (node[0] + 1, node[1] + 1)
        elif incoming_direction == 3:
            if outgoing_direction == 4:
                if self.clockwise:
                    buffered_node = (node[0] + 1, node[1] + 1)
                else:
                    buffered_node = (node[0] - 1, node[1] - 1)
            elif outgoing_direction == 2:
                if self.clockwise:
                    buffered_node = (node[0] + 1, node[1] - 1)
                else:
                    buffered_node = (node[0] - 1, node[1] + 1)
        elif incoming_direction == 4:
            if outgoing_direction == 1:
                if self.clockwise:
                    buffered_node = (node[0] - 1, node[1] + 1)
                else:
                    buffered_node = (node[0] + 1, node[1] - 1)
            elif outgoing_direction == 3:
                if self.clockwise:
                    buffered_node = (node[0] + 1, node[1] + 1)
                else:
                    buffered_node = (node[0] - 1, node[1] - 1)

        return buffered_node


class Grid:
    """ grid object where red or green cell = 1 """
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((self.height, self.width), dtype=np.int32)

    def draw_polygon(self, polygon: Polygon):
        node_list = polygon.node_list
        first_node = node_list[0]
        for i, node in enumerate(node_list):
            # wrap to first node at end
            if i == len(node_list) - 1:
                next_node = first_node
            else:
                next_node = node_list[i + 1]
            self._draw_line(node, next_node)

    def check_rectangle(self, rectangle: Rectangle) -> bool:
        x1, y1, x2, y2 = rectangle.x1, rectangle.y1, rectangle.x2, rectangle.y2
        y_min, y_max = min(y1, y2), max(y1, y2)
        x_min, x_max = min(x1, x2), max(x1, x2)
        arr = self.grid[y_min:y_max + 1, x_min:x_max + 1]
        return not arr.any()

    def _draw_line(self, node1: tuple[int, int], node2: tuple[int, int]):
        x1, y1 = node1
        x2, y2 = node2

        y_min = min(y1, y2)
        y_max = max(y1, y2)
        x_min = min(x1, x2)
        x_max = max(x1, x2)

        self.grid[y_min:y_max+1, x_min:x_max+1] = 1


def strip_lines(lines_list: list[str]) -> list[str]:
    stripped_lines_list = []
    for item in lines_list:
        stripped_lines_list.append(item.strip())
    return stripped_lines_list


def convert_node_list(node_list: list[str]) -> list[tuple[int, int]]:
    node_list_corrected = []
    for node in node_list:
        x, y = node.split(',')
        node_corrected = (int(x), int(y))
        node_list_corrected.append(node_corrected)

    return node_list_corrected



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

    # convert node list to tuple[int, int]
    node_list = convert_node_list(node_list)

    node_list_original = list(node_list)

    # iterate over every combination of nodes and create list of tuples in form (area, Rectangle)
    rectangle_tuples = []
    max_x = 0
    max_y = 0
    while True:
        current_node = node_list.pop()
        for node in node_list:
            rectangle = Rectangle(current_node, node)
            rectangle_tuples.append((rectangle.area, rectangle))
            # track max x and y values
            max_x = max(max_x, rectangle.x1, rectangle.x2)
            max_y = max(max_y, rectangle.y1, rectangle.y2)
        if len(node_list) == 0:
            break

    # sort rectangle tuples from largest to smallest
    sorted_rectangle_tuples = sorted(rectangle_tuples, key=lambda n: n[0], reverse=True)

    # build polygon
    polygon = Polygon(node_list_original)

    # build buffered polygon
    buffered_polygon = polygon.buffer_polygon()

    # build grid
    grid = Grid(max_x + 2, max_y + 2)
    grid.draw_polygon(buffered_polygon)

    # print(grid.grid)

    # find biggest rectangle which doesn't have a 1
    print(f'Number of rectangles to check: {len(sorted_rectangle_tuples)}')
    i = 0
    for area, rectangle in sorted_rectangle_tuples:
        i += 1
        print(f'Checking rectangle {i} of {len(sorted_rectangle_tuples)}')
        # early check - continue if the rectangle has another vertex inside
        internal_vertex_count = rectangle.count_internal_vertices(node_list_original)
        if internal_vertex_count > 0:
            continue
        # second check. Quite slow
        fully_internal = grid.check_rectangle(rectangle)
        if fully_internal:
            break

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Max area: {area}')


if __name__ == "__main__":
    main()
