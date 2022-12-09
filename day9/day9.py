R = 500


def main(input_filename, num_knots):
    with open(input_filename) as input_file:
        instructions = [line.strip().split(' ') for line in input_file.readlines()]
    return simulate_knots(instructions, num_knots)


def simulate_knots(instructions, num_knots):
    grid = [[False for _ in range(2 * R)] for _ in range(2 * R)]
    knots = [[R, R] for _ in range(num_knots)]
    grid[knots[-1][0]][knots[-1][1]] = True
    for direction, steps in instructions:
        for _ in range(int(steps)):
            move_head_knot(knots[0], direction)
            [move_knot(knots[i], knots[i + 1]) for i in range(num_knots - 1)]
            grid[knots[-1][0]][knots[-1][1]] = True
    return sum([1 for row in grid for position in row if position])


def move_head_knot(knot, direction):
    if direction == 'U':
        knot[1] -= 1
    elif direction == 'D':
        knot[1] += 1
    elif direction == 'L':
        knot[0] -= 1
    else:
        knot[0] += 1


def move_knot(head, tail):
    if head[0] < tail[0] - 1:
        tail[0] -= 1
        if head[1] != tail[1]:
            tail[1] = head[1]
    elif head[0] > tail[0] + 1:
        tail[0] += 1
        if head[1] != tail[1]:
            tail[1] = head[1]
    elif head[1] < tail[1] - 1:
        tail[1] -= 1
        if head[0] != tail[0]:
            tail[0] = head[0]
    elif head[1] > tail[1] + 1:
        tail[1] += 1
        if head[0] != tail[0]:
            tail[0] = head[0]


if __name__ == '__main__':
    print(main('test1.txt', 2))
    print(main('input.txt', 2))
    print(main('test1.txt', 10))
    print(main('test2.txt', 10))
    print(main('input.txt', 10))
