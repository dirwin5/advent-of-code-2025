import pathlib
from time import time

def rotate(start_position: int,
           direction: str,
           distance: int) -> tuple[int, int]:
    if direction == 'R':
        new_position = start_position + distance
    elif direction == 'L':
        new_position = start_position - distance
    else:
        raise ValueError("Direction must be 'R' or 'L'")
    zero_passes = abs(new_position // 100)
    # catch edge case where starting at 0 and moving left
    if start_position == 0 and direction == 'L':
        zero_passes -= 1
    new_position = new_position % 100
    # catch edge case where ending at 0 and moving left
    if new_position == 0 and direction == 'L':
        zero_passes += 1
    return new_position, zero_passes

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

    position = 50
    counter = 0

    for rotation in data_list:
        rotation = rotation.strip()
        if len(rotation) == 0:
            break
        direction = rotation[0]
        distance = int(rotation[1:])
        print(f'Starting at {position} rotate {rotation}')
        position, zero_passes = rotate(position, direction, distance)
        print(f'New position {position}, passed zero {zero_passes} times')
        counter += zero_passes
        print(f'Counter now {counter}\n')

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Final Position: {position}')
    print(f'Total zero passes: {counter}')


if __name__ == "__main__":
    main()