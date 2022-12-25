def main(input_file_name, get_snacks):
    with open(input_file_name) as input_file:
        lines = [line.strip() for line in input_file.readlines() if line != '\n']

    width = len(lines[0]) - 2
    height = len(lines) - 2
    x_blizzards = []
    y_blizzards = []
    for y, row in enumerate([line.strip('#') for line in lines[1:-1]]):
        for x, value in enumerate(row):
            if value == '<':
                x_blizzards.append((x, y, -1))
            elif value == '>':
                x_blizzards.append((x, y, 1))
            elif value == '^':
                y_blizzards.append((x, y, -1))
            elif value == 'v':
                y_blizzards.append((x, y, 1))

    getting_snacks = False
    got_snacks = not get_snacks

    first_trip_time = 0
    snack_get_time = 0

    possible_positions = {0: {(0, -1)}}
    for minute in range(1, 1000000):
        x_blizzards = [((x + direction) % width, y, direction) for (x, y, direction) in x_blizzards]
        y_blizzards = [(x, (y + direction) % height, direction) for (x, y, direction) in y_blizzards]

        if minute == first_trip_time:
            possible_positions[minute] = {(width - 1, height)}
            getting_snacks = True
            continue
        elif minute == snack_get_time:
            possible_positions[minute] = {(0, -1)}
            getting_snacks = False
            got_snacks = True
            continue

        grid = [[False for _ in range(height)] for _ in range(width)]
        for (x, y, _) in x_blizzards + y_blizzards:
            grid[x][y] = True

        possible_positions[minute] = set()
        for (x, y) in possible_positions[minute - 1]:
            if x - 1 >= 0 and 0 <= y < height and not grid[x - 1][y]:
                if getting_snacks and x - 1 == 0 and y == 0:
                    snack_get_time = minute + 1
                    break
                possible_positions[minute].add((x - 1, y))
            if x + 1 < width and 0 <= y < height and not grid[x + 1][y]:
                if not getting_snacks and x + 1 == width - 1 and y == height - 1:
                    if got_snacks:
                        return minute + 1
                    else:
                        first_trip_time = minute + 1
                        break
                possible_positions[minute].add((x + 1, y))
            if y - 1 >= 0 and not grid[x][y - 1]:
                if getting_snacks and x == 0 and y - 1 == 0:
                    snack_get_time = minute + 1
                    break
                possible_positions[minute].add((x, y - 1))
            if y + 1 < height and not grid[x][y + 1]:
                if not getting_snacks and x == width - 1 and y + 1 == height - 1:
                    if got_snacks:
                        return minute + 1
                    else:
                        first_trip_time = minute + 1
                        break
                possible_positions[minute].add((x, y + 1))
            if y < 0 or y == height or not grid[x][y]:
                possible_positions[minute].add((x, y))


if __name__ == '__main__':
    print(main('test.txt', False))
    print(main('input.txt', False))
    print(main('test.txt', True))
    print(main('input.txt', True))
