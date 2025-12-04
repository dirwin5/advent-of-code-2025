import pathlib
from time import time

def rotate(start_position: int,
           direction: str,
           distance: int) -> int:
    if direction == 'R':
        new_position = (start_position + distance) % 100
    elif direction == 'L':
        new_position = (start_position - distance) % 100
    else:
        raise ValueError("Direction must be 'R' or 'L'")
    return new_position

def main():
    start_time = time()

    # get input file path
    cwd = pathlib.Path(__file__).parent
    input_dir = cwd.joinpath('input')
    input_file = input_dir.joinpath('input.txt')

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
        position = rotate(position, direction, distance)
        if position == 0:
            counter += 1

    print(f'Process Complete: Total time: {round(time() - start_time, 2)} seconds')
    print(f'Final Position: {position}')
    print(f'Total zeros: {counter}')


if __name__ == "__main__":
    main()