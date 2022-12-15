import re


def main(input_file_name, y):
    with open(input_file_name) as input_file:
        lines = [line.strip() for line in input_file.readlines() if line != '\n']

    x = []
    beacon_x = []
    for line in lines:
        [s_x, s_y, b_x, b_y] = [int(n) for n in re.findall(r'-?\d+\.?\d*', line)]
        b_dist = abs(s_x - b_x) + abs(s_y - b_y)
        y_dist = abs(s_y - y)
        if b_dist >= y_dist:
            x_dist = b_dist - y_dist
            x += [n + s_x for n in range(-x_dist, x_dist + 1)]

        if b_y == y:
            beacon_x.append(b_x)

    unique_x = set(x)
    for b_x in beacon_x:
        if b_x in unique_x:
            unique_x.remove(b_x)

    return len(unique_x)


if __name__ == '__main__':
    print(main('test.txt', 10))
    print(main('input.txt', 2000000))
