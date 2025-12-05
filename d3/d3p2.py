"""
https://adventofcode.com/2025/day/3
"""
import pathlib
from time import time


def find_largest_digit_in_segment(bank_segment):
    largest_index = 0
    largest_value = bank_segment[largest_index]
    for digit_index, digit in enumerate(bank_segment):
        if digit_index == 0:
            continue
        if int(digit) > int(largest_value):
            largest_index = digit_index
            largest_value = digit

    return largest_index


def find_max_number(bank: str, required_length: int) -> int:
    number = ''
    count_to_exclude = len(bank) - required_length
    i = 0
    while True:
        # check first {count_to_exclude} + 1 characters and find largest number
        bank_segment = bank[i:i + count_to_exclude + 1]
        largest_digit_in_segment_index = find_largest_digit_in_segment(bank_segment)
        number += bank_segment[largest_digit_in_segment_index]
        count_to_exclude -= largest_digit_in_segment_index
        i += largest_digit_in_segment_index + 1
        if count_to_exclude == 0:
            # add the remaining digits from bank
            number += bank[i:]
        if len(number) >= required_length:
            break

    return int(number)


def main(required_length: int = 2):
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
        max_joltage = find_max_number(bank.strip(), required_length)
        print(max_joltage)
        counter += max_joltage

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {counter}')


if __name__ == "__main__":
    main(required_length=12)
