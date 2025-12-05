import pathlib
from time import time


def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')

    # read input file
    with open(input_file, 'r') as f:
        range_list = f.read().split(',')

    counter = 0
    for range in range_list:
        range = range.strip()
        range_items = range.split('-')
        range_start = range_items[0]
        range_end = range_items[1]

        # check number of digits and discard ranges with start and end of same length and
        # odd number of digits
        if len(range_start) == len(range_end) and len(range_start) % 2 != 0:
            continue

        # if start range has odd number of digits, increase to next number with
        # even number of digits
        if len(range_start) % 2 != 0:
            range_start = '1' + '0' * len(range_start)

        # current_id = range_start[:len(range_start)//2]
        current_id = range_start
        current_half = current_id[:len(current_id) // 2]
        while True:
            invalid_id = current_half * 2
            if int(range_start) <= int(invalid_id) <= int(range_end):
                counter += int(invalid_id)
            current_half = str(int(current_half) + 1)
            if int(current_half * 2) > int(range_end):
                break

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {counter}')


if __name__ == "__main__":
    main()
