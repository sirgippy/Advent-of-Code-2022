from json import dumps, loads

directions = [
    [[0, -1], [1, -1], [-1, -1]],
    [[0, 1], [1, 1], [-1, 1]],
    [[-1, 0], [-1, -1], [-1, 1]],
    [[1, 0], [1, -1], [1, 1]]
]


def main(input_file_name, rounds=None):
    with open(input_file_name) as input_file:
        lines = [line.strip() for line in input_file.readlines() if line != '\n']

    elves = {}
    next_elf = 1

    for row_idx, row in enumerate(lines):
        for column_idx, tile in enumerate(row):
            if tile == '#':
                elves[next_elf] = [column_idx, row_idx]
                next_elf += 1

    if rounds is None:
        rounds = 1000000000

    prev_round = loads(dumps(elves))
    move_round = 0
    for move_round in range(rounds):
        round_directions = directions[move_round % 4:] + directions[:move_round % 4]
        proposed_movements = {}
        for elf, position in elves.items():
            move = False
            for x, y in [[c, r] for c in range(-1, 2) for r in range(-1, 2) if [c, r] != [0, 0]]:
                if [position[0] + x, position[1] + y] in elves.values():
                    move = True
                    break
            if not move:
                continue
            for direction in round_directions:
                if (
                    [position[0] + direction[0][0], position[1] + direction[0][1]] not in elves.values()
                    and [position[0] + direction[1][0], position[1] + direction[1][1]] not in elves.values()
                    and [position[0] + direction[2][0], position[1] + direction[2][1]] not in elves.values()
                ):
                    proposed_movements[elf] = [position[0] + direction[0][0], position[1] + direction[0][1]]
                    break
        for elf, new_position in proposed_movements.items():
            if list(proposed_movements.values()).count(new_position) < 2:
                elves[elf] = new_position
        if all([pos in prev_round.values() for pos in elves.values()]):
            break
        else:
            prev_round = loads(dumps(elves))

    xs = [pos[0] for pos in elves.values()]
    ys = [pos[1] for pos in elves.values()]
    return (max(xs) - min(xs) + 1) * (max(ys) - min(ys) + 1) - len(elves), move_round + 1


if __name__ == '__main__':
    print(main('test1.txt', 3))
    print(main('test2.txt', 10))
    print(main('input.txt', 10))
    print(main('test2.txt'))
    print(main('input.txt'))
