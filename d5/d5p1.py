"""
https://adventofcode.com/2025/day/5
"""
import pathlib
from time import time
import bisect


def split_data_list(data_list: list, split_on: str) -> tuple[list, list]:
    # find index of split_on
    index = data_list.index(split_on)
    list1 = data_list[:index]
    list2 = data_list[index + 1 :]
    return list1, list2


def consolidate_ranges(range_list: list[tuple[int, int]]) -> tuple[list[tuple[int, int]], bool]:
    consolidated_range_list = []
    skip_next = False
    for i, (start, end) in enumerate(range_list):
        if skip_next:
            skip_next = False
            continue
        try:
            next_start = range_list[i + 1][0]
            next_end = range_list[i + 1][1]
        except IndexError:
            consolidated_range_list.append((start, end))
            break
        if end >= next_start - 1:
            consolidated_range_list.append((start, max(next_end, end)))
            # if start == next_end:
            #     pass
            skip_next = True
            continue
        consolidated_range_list.append((start, end))

    changed = len(range_list) != len(consolidated_range_list)

    return consolidated_range_list, changed


def convert_range_list_to_tuples(range_list: list[str]) -> list[tuple[int, int]]:
    """
    Convert a list of range strings into a list of int tuples.
    E.g. '3-5' becomes (3, 5)
    """
    range_list_tuples = []
    for range_string in range_list:
        split_string = range_string.split('-')
        range_tuple = (int(split_string[0]), int(split_string[1]))
        range_list_tuples.append(range_tuple)

    return range_list_tuples


def check_if_id_is_in_range(ingredient_id: int,
                            sorted_range_list: list[tuple[int, int]],
                            range_start_list: list[int]) -> bool:
    # find index of range with starting value equal to or lower than ingredient_id
    index = bisect.bisect(range_start_list, ingredient_id) - 1
    # check if value is in range
    range_start, range_end = sorted_range_list[index]
    if range_start <= ingredient_id <= range_end:
        # print(f'id: {ingredient_id}, True, Range start: {range_start}, end: {range_end}')
        return True
    # print(f'id: {ingredient_id}, False, Range start: {range_start}, end: {range_end}')
    return False


def check_if_id_is_in_range_brute_force(ingredient_id: int,
                                        range_list: list[tuple[int, int]]) -> bool:
    """ Brute force version - used during debugging """
    for range_start, range_end in range_list:
        if range_start <= ingredient_id <= range_end:
            # print(f'id: {ingredient_id}, True, Range start: {range_start}, end: {range_end}')
            return True
    # print(f'id: {ingredient_id}, False')
    return False


def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')
    # input_file = input_dir.joinpath('sample_input.txt')

    # read input file
    with open(input_file, 'r') as f:
        data_list = f.readlines()

    # strip each item in data_list
    stripped_data_list = []
    for item in data_list:
        stripped_data_list.append(item.strip())

    # split data_list into range_list and id_list
    range_list, id_list = split_data_list(stripped_data_list, '')

    # convert range_list into list of tuples
    range_list_tuples = convert_range_list_to_tuples(range_list)

    # sort ranges
    sorted_range_list = sorted(range_list_tuples, key=lambda x: x[0])

    # consolidate ranges. Iterate until no change as only two ranges are merged at a time
    while True:
        consolidated_range_list, changed = consolidate_ranges(sorted_range_list)
        sorted_range_list = consolidated_range_list.copy()
        sorted_range_list = sorted(sorted_range_list, key=lambda x: x[0])
        if not changed:
            break

    # make list of range start values
    range_start_list = []
    for range_tuple in sorted_range_list:
        range_start_list.append(range_tuple[0])

    # find how many ids fall within a range
    counter = 0
    for ingredient_id in id_list:
        fresh = check_if_id_is_in_range(int(ingredient_id), sorted_range_list, range_start_list)
        if fresh:
            counter += 1

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Total: {counter}')


if __name__ == "__main__":
    main()
