from math import floor, prod


def main(input_file_name, rounds, reduce_worry):
    monkeys = parse_input(input_file_name)
    inspection_counts = chase_monkeys(monkeys, rounds, reduce_worry)
    sorted_counts = sorted([inspections for inspections in inspection_counts.values()], reverse=True)
    return sorted_counts[0] * sorted_counts[1]


def parse_input(input_file_name):
    with open(input_file_name) as input_file:
        lines = input_file.readlines()
    monkeys = {}
    for i in range(0, len(lines), 7):
        monkey = parse_monkey(lines[i:i + 6])
        monkeys[monkey['id']] = monkey
    return monkeys


def parse_monkey(lines):
    return {
        'id': int(lines[0][7]),
        'items': [int(item) for item in lines[1][18:].strip().split(', ')],
        'operation': lines[2][19:].strip().split(' '),
        'test': int(lines[3][21:].strip()),
        'if_true': int(lines[4][29]),
        'if_false': int(lines[5][30])
    }


def chase_monkeys(monkeys, rounds, reduce_worry=True):
    inspection_counts = {i: 0 for i in range(len(monkeys))}
    test_product = prod([monkey['test'] for monkey in monkeys.values()])
    for _ in range(rounds):
        for i in range(len(monkeys)):
            monkey = monkeys[i]
            for item in monkey['items']:
                inspection_counts[i] += 1
                if monkey['operation'][1] == '*':
                    if monkey['operation'][2] == 'old':
                        item = item * item
                    else:
                        item = item * int(monkey['operation'][2])
                else:
                    if monkey['operation'][2] == 'old':
                        item = item + item
                    else:
                        item = item + int(monkey['operation'][2])
                if reduce_worry:
                    item = floor(item / 3)
                else:
                    item = item % test_product
                if item % monkey['test'] == 0:
                    monkeys[monkey['if_true']]['items'].append(item)
                else:
                    monkeys[monkey['if_false']]['items'].append(item)
            monkey['items'] = []
    return inspection_counts


if __name__ == '__main__':
    print(main('test.txt', 20, True))
    print(main('input.txt', 20, True))
    print(main('test.txt', 10000, False))
    print(main('input.txt', 10000, False))
