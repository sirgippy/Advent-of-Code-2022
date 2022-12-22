facings = [(0, 1), (1, 0), (0, -1), (-1, 0)]
cube_edges = [
    [[[0, c] for c in range(50, 100)], 3, [[r, 0] for r in range(150, 200)], 2],
    [[[0, c] for c in range(100, 150)], 3, [[199, c] for c in range(0, 50)], 1],
    [[[r, 149] for r in range(0, 50)], 0, [[r, 99] for r in range(149, 99, -1)], 0],
    [[[49, c] for c in range(100, 150)], 1, [[r, 99] for r in range(50, 100)], 0],
    [[[149, c] for c in range(50, 100)], 1, [[r, 49] for r in range(150, 200)], 0],
    [[[r, 50] for r in range(0, 50)], 2, [[r, 0] for r in range(149, 99, -1)], 2],
    [[[r, 50] for r in range(50, 100)], 2, [[100, c] for c in range(0, 50)], 3]
]


def main(input_file_name, is_cube=False):
    grid = []
    with open(input_file_name) as input_file:
        line = input_file.readline()
        while line != '\n':
            grid.append(line.strip('\n'))
            line = input_file.readline()

        directions = input_file.readline().strip('\n')

    add_buffers_to_grid(grid)
    directions = parse_directions(directions)

    position = [0, grid[0].find('.')]
    facing_idx = 0
    facing = facings[facing_idx]

    for direction in directions:
        if type(direction) == int:
            position, facing_idx = move(position, facing_idx, grid, direction, is_cube)
        else:
            if direction == 'L':
                facing_idx = (facing_idx - 1) % len(facings)
            else:
                facing_idx = (facing_idx + 1) % len(facings)

    return (position[0] + 1) * 1000 + (position[1] + 1) * 4 + facing_idx


def move(position, facing_idx, grid, steps, is_cube):
    done_moving = False
    remaining_steps = steps
    new_position = position
    new_facing_idx = facing_idx
    while not done_moving:
        facing = facings[facing_idx]
        new_position = [(new_position[0] + facing[0]) % len(grid), (new_position[1] + facing[1]) % len(grid[0])]
        if is_cube and grid[new_position[0]][new_position[1]] == ' ':
            new_position, new_facing_idx = wrap_cube(position, new_facing_idx)
        if grid[new_position[0]][new_position[1]] == '#':
            done_moving = True
            new_facing_idx = facing_idx
        elif grid[new_position[0]][new_position[1]] == '.':
            position = new_position
            facing_idx = new_facing_idx
            remaining_steps -= 1
            if remaining_steps == 0:
                done_moving = True
    return position, facing_idx


def wrap_cube(position, facing_idx):
    new_position = None
    new_facing_idx = None
    for edge in cube_edges:
        if position in edge[0] and facing_idx == edge[1]:
            new_position = edge[2][edge[0].index(position)]
            new_facing_idx = (edge[3] + 2) % 4
        elif position in edge[2] and facing_idx == edge[3]:
            new_position = edge[0][edge[2].index(position)]
            new_facing_idx = (edge[1] + 2) % 4
    if not new_position:
        raise ValueError('nope')
    return new_position, new_facing_idx


def add_buffers_to_grid(grid):
    max_length = max([len(row) for row in grid])
    for idx, row in enumerate(grid):
        grid[idx] += ' ' * (max_length - len(row))


def parse_directions(raw_directions):
    directions = []
    next_number = ''
    for char in raw_directions:
        if char == 'R' or char == 'L':
            if next_number != '':
                directions.append(int(next_number))
                next_number = ''
            directions.append(char)
        else:
            next_number += char
    if next_number != '':
        directions.append(int(next_number))
    return directions


if __name__ == '__main__':
    print(main('test.txt'))
    print(main('input.txt'))
    print(main('input.txt', True))
