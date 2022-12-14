from day14a import get_rocks

X_MAX_OFFSET = 200


def main(input_file_name):
    with open(input_file_name) as input_file:
        rock_paths = [line.strip() for line in input_file.readlines()]

    grid = create_grid(rock_paths)
    sand = add_sand(grid)

    return sand


def create_grid(rock_paths):
    rocks = get_rocks(rock_paths)

    x_max = max([rock[0] for rock in rocks]) + X_MAX_OFFSET
    y_max = max([rock[1] for rock in rocks]) + 2

    grid = [['.' for _ in range(y_max + 1)] for _ in range(x_max + 1)]
    for rock in rocks:
        grid[rock[0]][rock[1]] = '#'
    for x in range(x_max + 1):
        grid[x][y_max] = '#'

    return grid


def add_sand(grid):
    sand = 0
    full = False
    while not full:
        sand_pos = [500, 0]
        while True:
            sand_pos[1] += 1
            if grid[sand_pos[0]][sand_pos[1]] == '.':
                continue
            elif grid[sand_pos[0] - 1][sand_pos[1]] == '.':
                sand_pos[0] -= 1
                continue
            elif grid[sand_pos[0] + 1][sand_pos[1]] == '.':
                sand_pos[0] += 1
                continue
            else:
                sand += 1
                grid[sand_pos[0]][sand_pos[1] - 1] = 'o'
                if sand_pos[1] - 1 == 0:
                    full = True
                break
    return sand


if __name__ == '__main__':
    print(main('test.txt'))
    print(main('input.txt'))
