import pathlib
from time import time


def assess_range(range_start: str, range_end: str) -> list[int]:
    invalid_ids = []
    min_digits = len(range_start)
    max_digits = len(range_end)

    for sequence_len in range(1, (max_digits // 2) + 1):
        current_sequence = '1' + '0' * (sequence_len - 1)
        first_repetitions = min_digits // sequence_len
        while True:
            current_repetitions = first_repetitions
            while True:
                invalid_id = current_sequence * current_repetitions
                if int(invalid_id) > int(range_end):
                    break
                if int(range_start) <= int(invalid_id) <= int(range_end) and len(invalid_id) > 1:
                    invalid_ids.append(int(invalid_id))
                current_repetitions += 1

            current_sequence = str(int(current_sequence) + 1)
            if len(current_sequence) > sequence_len:
                break

    return invalid_ids


def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')
    # input_file = input_dir.joinpath('sample_input.txt')

    # read input file
    with open(input_file, 'r') as f:
        range_list = f.read().split(',')

    invalid_ids = []
    for range in range_list:
        range = range.strip()
        range_items = range.split('-')
        range_start = range_items[0]
        range_end = range_items[1]

        range_invalid_ids = assess_range(range_start, range_end)
        invalid_ids.extend(range_invalid_ids)

        print(f'{range_start}-{range_end}: {range_invalid_ids}')

    # remove duplicates
    invalid_ids = list(set(invalid_ids))
    print(f'\nInvalid IDs: {sorted(invalid_ids)}')

    total = sum(invalid_ids)

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {total}')


if __name__ == "__main__":
    main()
