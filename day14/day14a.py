def main(input_file_name):
    with open(input_file_name) as input_file:
        rock_paths = [line.strip() for line in input_file.readlines()]

    grid, x_offset = create_grid(rock_paths)
    sand = add_sand(grid, x_offset)

    return sand


def create_grid(rock_paths):
    rocks = get_rocks(rock_paths)

    x_offset = min([rock[0] for rock in rocks])
    x_max = max([rock[0] for rock in rocks]) - x_offset
    y_max = max([rock[1] for rock in rocks])

    grid = [['.' for _ in range(y_max + 1)] for _ in range(x_max + 1)]
    for rock in rocks:
        grid[rock[0] - x_offset][rock[1]] = '#'

    return grid, x_offset


def get_rocks(rock_paths):
    rocks = []
    for path in rock_paths:
        vertices = [[int(dim) for dim in vertex.split(',')] for vertex in path.split(' -> ')]
        prev_vertex = vertices[0]
        rocks.append(prev_vertex)
        for vertex in vertices[1:]:
            if vertex[0] > prev_vertex[0]:
                rocks += [[prev_vertex[0] + idx + 1, vertex[1]] for idx in range(0, vertex[0] - prev_vertex[0])]
            elif vertex[0] < prev_vertex[0]:
                rocks += [[prev_vertex[0] + idx - 1, vertex[1]] for idx in range(0, vertex[0] - prev_vertex[0], -1)]
            elif vertex[1] > prev_vertex[1]:
                rocks += [[vertex[0], prev_vertex[1] + idx + 1] for idx in range(0, vertex[1] - prev_vertex[1])]
            else:
                rocks += [[vertex[0], prev_vertex[1] + idx - 1] for idx in range(0, vertex[1] - prev_vertex[1], -1)]
            prev_vertex = vertex
    return rocks


def add_sand(grid, x_offset):
    sand_start_x = 500 - x_offset

    sand = 0
    full = False
    while not full:
        sand_pos = [sand_start_x, 0]
        while True:
            sand_pos[1] += 1
            if sand_pos[1] == len(grid[0]):
                full = True
                break
            elif grid[sand_pos[0]][sand_pos[1]] == '.':
                continue
            elif sand_pos[0] - 1 < 0:
                full = True
                break
            elif grid[sand_pos[0] - 1][sand_pos[1]] == '.':
                sand_pos[0] -= 1
                continue
            elif sand_pos[0] + 1 > len(grid):
                full = True
                break
            elif grid[sand_pos[0] + 1][sand_pos[1]] == '.':
                sand_pos[0] += 1
                continue
            else:
                sand += 1
                grid[sand_pos[0]][sand_pos[1] - 1] = 'o'
                break
    return sand


if __name__ == '__main__':
    print(main('test.txt'))
    print(main('input.txt'))
