"""
https://adventofcode.com/2025/day/3

d3p2.py can also solve this and uses a better approach
"""
import pathlib
from time import time
import re


def find_digit(bank: str, digit_to_find: str, max_index: int, min_index: int=0) -> None | int:
    for match in re.finditer(digit_to_find, bank):
        if min_index <= match.start() < max_index:
            return match.start()

    return None


def find_max_number(bank: str) -> int:
    number = ''
    i = 9
    # first digit
    while True:
        # can't be last character
        index = find_digit(bank, str(i), len(bank) - 1)
        if index is None:
            i -= 1
            continue
        else:
            number += str(bank[index])
            break

    # second digit
    min_index = index + 1
    i = 9
    while True:
        index = find_digit(bank, str(i), len(bank), min_index)
        if index is None:
            i -= 1
            continue
        else:
            number += str(bank[index])
            break

    return int(number)


def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')
    # input_file = input_dir.joinpath('sample_input.txt')

    # read input file
    with open(input_file, 'r') as f:
        bank_list = f.readlines()

    counter = 0
    for bank in bank_list:
        max_joltage = find_max_number(bank.strip())
        print(max_joltage)
        counter += max_joltage

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {counter}')


if __name__ == "__main__":
    main()
