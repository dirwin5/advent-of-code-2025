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


def strip_newlines(lines_list: list[str]) -> list[str]:
    """ Only remove newline characters. Keep other leading and trailing whitespace """
    stripped_lines_list = []
    for item in lines_list:
        stripped_lines_list.append(item.replace("\n", ""))
    return stripped_lines_list


def solve_answer(numbers_list: list[int], operator: str):
    if operator == '+':
        answer = sum(numbers_list)
    elif operator == '*':
        answer = math.prod(numbers_list)
    else:
        raise ValueError(f'Unknown operator: {operator}')
    return answer


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
    stripped_lines_list = strip_newlines(lines_list)

    # last line contains the operators
    operator_row_index = len(stripped_lines_list) - 1

    # make sure all rows are the same length and have 1 empty space
    longest_line = 0
    for line in stripped_lines_list:
        longest_line = max(longest_line, len(line))
    required_length = longest_line + 1
    input_lines_list = []
    for row in stripped_lines_list:
        required_whitespace = required_length - len(row)
        row += ' ' * required_whitespace
        input_lines_list.append(row)

    total = 0
    numbers_list = []
    number = ''
    for col in range(len(input_lines_list[0])):
        if input_lines_list[operator_row_index][col].strip():
            operator = input_lines_list[operator_row_index][col]
        for row in range(operator_row_index):
            number += input_lines_list[row][col]

        # if column isn't empty, add number and move onto next column
        if number.strip():
            numbers_list.append(int(number))
            number = ''
        # if column is empty, solve this problem and reset
        else:
            answer = solve_answer(numbers_list, operator)
            # print(f'Answer: {answer}')
            total += answer
            numbers_list = []
            number = ''


    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {total}')


if __name__ == "__main__":
    main()
