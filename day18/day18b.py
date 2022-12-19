def main(input_file_name):
    with open(input_file_name) as input_file:
        droplet = [
            [int(coord) for coord in line.strip().split(',')]
            for line in input_file.readlines() if line != '\n'
        ]
    air = find_air(droplet)
    return count_exposed_sides(air, droplet)


def find_air(droplet):
    max_x = max([cube[0] for cube in droplet]) + 1
    max_y = max([cube[1] for cube in droplet]) + 1
    max_z = max([cube[2] for cube in droplet]) + 1
    air = [[[False for _ in range(0, max_z + 1)] for _ in range(0, max_y + 1)] for _ in range(0, max_x + 1)]
    air[0][0][0] = True
    check_queue = [(0, 0, 0)]
    while check_queue:
        (x, y, z) = check_queue.pop(0)
        for (dx, dy, dz) in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            if (
                    0 <= x + dx <= max_x
                    and 0 <= y + dy <= max_y
                    and 0 <= z + dz <= max_z
                    and not air[x + dx][y + dy][z + dz]
                    and [x + dx, y + dy, z + dz] not in droplet
            ):
                air[x + dx][y + dy][z + dz] = True
                check_queue.append((x + dx, y + dy, z + dz))
    return air


def count_exposed_sides(air, droplet):
    sides = 0
    for cube in droplet:
        for (dx, dy, dz) in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
            if air[cube[0] + dx][cube[1] + dy][cube[2] + dz]:
                sides += 1
    return sides


if __name__ == '__main__':
    print(main('test.txt'))
    print(main('input.txt'))
