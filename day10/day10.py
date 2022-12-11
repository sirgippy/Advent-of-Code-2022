def main(input_file_name):
    with open(input_file_name) as input_file:
        instructions = [line.strip() for line in input_file.readlines()]
    cycle_history = get_cycle_history(instructions)
    print_crt(cycle_history)
    return sum([idx * cycle_history[idx - 1] for idx in range(20, 221, 40)])


def get_cycle_history(instructions):
    x = 1
    cycle_history = []
    for instruction in instructions:
        if instruction[0:4] == 'addx':
            v = int(instruction[5:])
            cycle_history.append(x)
            cycle_history.append(x)
            x += v
        else:
            cycle_history.append(x)
    return cycle_history


def print_crt(cycle_history):
    for idx in range(0, len(cycle_history), 40):
        print_row(cycle_history[idx: idx+40])


def print_row(row_x_values):
    row = ''
    for i, x in enumerate(row_x_values):
        if abs(x - i) <= 1:
            row += '#'
        else:
            row += '.'
    print(row)


if __name__ == '__main__':
    print(main('test.txt'))
    print(main('input.txt'))
