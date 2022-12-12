def main(input_file_name, set_start=True):
    with open(input_file_name) as input_file:
        heightmap = [[char for char in line.strip()] for line in input_file.readlines()]
    start_pos = get_start(heightmap)
    finish_pos = get_finish(heightmap)

    if set_start:
        return find_shortest_path(heightmap, start_pos, finish_pos)
    else:
        return min([
            find_shortest_path(heightmap, pos, finish_pos) for pos in [
                [r, c] for r in range(len(heightmap)) for c in range(len(heightmap[0])) if heightmap[r][c] == 'a'
            ]
        ])


def find_shortest_path(heightmap, start_pos, finish_pos):

    shortest_path = [[-1 for _ in range(len(heightmap[0]))] for _ in range(len(heightmap))]
    current_distance = 0
    next_squares = [start_pos]
    shortest_path[start_pos[0]][start_pos[1]] = 0

    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    while next_squares:
        current_squares = next_squares
        next_squares = []
        current_distance += 1
        for square in current_squares:
            for direction in directions:
                new_pos = [square[0] + direction[0], square[1] + direction[1]]
                if (
                    0 <= new_pos[0] < len(heightmap)
                    and 0 <= new_pos[1] < len(heightmap[0])
                    and shortest_path[new_pos[0]][new_pos[1]] == -1
                    and ord(heightmap[square[0]][square[1]]) >= ord(heightmap[new_pos[0]][new_pos[1]]) - 1
                ):
                    if new_pos == finish_pos:
                        return current_distance
                    next_squares.append(new_pos)
                    shortest_path[new_pos[0]][new_pos[1]] = current_distance
    return 1e6


def get_start(heightmap):
    for i, row in enumerate(heightmap):
        for j, elevation in enumerate(row):
            if elevation == 'S':
                heightmap[i][j] = 'a'
                return [i, j]


def get_finish(heightmap):
    for i, row in enumerate(heightmap):
        for j, elevation in enumerate(row):
            if elevation == 'E':
                heightmap[i][j] = 'z'
                return [i, j]


if __name__ == '__main__':
    print(main('test.txt', True))
    print(main('input.txt', True))
    print(main('test.txt', False))
    print(main('input.txt', False))
