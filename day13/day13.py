import json
from functools import cmp_to_key


def part1(input_file_name):
    with open(input_file_name) as input_file:
        lines = [line.strip() for line in input_file.readlines()]

    pairs = parse_pairs(lines)
    correctly_ordered_pairs = []
    for i, pair in enumerate(pairs):
        if is_correct_order(pair[0], pair[1]) == -1:
            correctly_ordered_pairs.append(i + 1)

    return sum(correctly_ordered_pairs)


def parse_pairs(lines):
    pairs = []
    for idx in range(0, len(lines), 3):
        left = json.loads(lines[idx])
        right = json.loads(lines[idx + 1])
        pairs.append([left, right])
    return pairs


def part2(input_file_name):
    with open(input_file_name) as input_file:
        lines = [line.strip() for line in input_file.readlines()]
    unsorted_list = [json.loads(line) for line in lines if line != '']

    div1 = [[2]]
    div2 = [[6]]

    unsorted_list.append(div1)
    unsorted_list.append(div2)

    sorted_list = sorted(unsorted_list, key=cmp_to_key(is_correct_order))

    return (sorted_list.index(div1) + 1) * (sorted_list.index(div2) + 1)


def is_correct_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left < right:
            return -1
        elif left > right:
            return 1
        return 0

    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]

    for (x, y) in zip(left, right):
        is_correct = is_correct_order(x, y)
        if is_correct != 0:
            return is_correct

    if len(left) < len(right):
        return -1
    elif len(left) > len(right):
        return 1

    return 0


if __name__ == '__main__':
    print(part1('test.txt'))
    print(part1('input.txt'))
    print(part2('test.txt'))
    print(part2('input.txt'))
