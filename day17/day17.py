import time
from math import floor

log = [[0, 0], [1, 0], [2, 0], [3, 0]]
plus = [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]]
angle = [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]]
stick = [[0, 0], [0, 1], [0, 2], [0, 3]]
block = [[0, 0], [1, 0], [0, 1], [1, 1]]

rocks = [log, plus, angle, stick, block]


def main(input_file_name, num_rocks):
    start = time.time()
    with open(input_file_name) as input_file:
        pattern = input_file.readline().strip()
    next_pattern_move = 0

    well = {0: [x for x in range(7)]}

    for rock_num in range(num_rocks):
        rock = get_next_rock(rock_num, well)
        done = False
        while not done:
            move_rock_horizontal(pattern[next_pattern_move], rock, well)
            next_pattern_move = next_pattern_move + 1 if (next_pattern_move + 1) % len(pattern) != 0 else 0
            done = move_rock_down(rock, well)
        for rock_bit in rock:
            if rock_bit[1] not in well.keys():
                well[rock_bit[1]] = []
            well[rock_bit[1]].append(rock_bit[0])
    print(time.time() - start)
    return max(well.keys())


def get_next_rock(rock_num, well):
    base_rock = rocks[rock_num % len(rocks)]
    well_height = max(well.keys())
    rock = []
    for base_rock_bit in base_rock:
        rock.append([base_rock_bit[0] + 2, base_rock_bit[1] + well_height + 4])
    return rock


def move_rock_horizontal(direction, rock, well):
    if direction == '<' and min(bit[0] for bit in rock) == 0:
        pass
    elif direction == '>' and max(bit[0] for bit in rock) == 6:
        pass
    else:
        check_well = min([bit[1] for bit in rock]) <= max(well.keys())
        can_move = True
        movement = -1 if direction == '<' else 1
        if check_well:
            for bit in rock:
                if bit[1] in well.keys() and bit[0] + movement in well[bit[1]]:
                    can_move = False
                    break
        if can_move:
            for bit in rock:
                bit[0] += movement


def move_rock_down(rock, well):
    for bit in rock:
        if bit[1] - 1 in well.keys() and bit[0] in well[bit[1] - 1]:
            return True
    for bit in rock:
        bit[1] -= 1
    return False


if __name__ == '__main__':
    print(main('test.txt', 2022))
    print(main('input.txt', 2022))
    print((main('test.txt', 71) - main('test.txt', 36)) * floor((1e12 - 36) / 35) + main('test.txt', 50))
    print(
        (main('input.txt', 1690 * 2) - main('input.txt', 1690)) * floor((1e12 - 1690) / 1690)
        + main('input.txt', int(1690 + (1e12 % 1690)))
    )
