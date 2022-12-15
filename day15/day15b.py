import re


class Row:
    def __init__(self, y, n_min, n_max):
        self.y = y
        self.n_min = n_min
        self.n_max = n_max
        self.ranges = []

    def add_range(self, start, finish):
        if start < self.n_min:
            start = self.n_min
        if finish > self.n_max:
            finish = self.n_max
        new_range = [start, finish]
        ranges_to_remove = []
        for x_range in self.ranges:
            if x_range[0] <= new_range[0] <= x_range[1] + 1:
                if new_range[1] <= x_range[1]:
                    new_range = None
                    break
                else:
                    ranges_to_remove.append(x_range)
                    new_range = [x_range[0], new_range[1]]
            elif x_range[0] <= new_range[1] <= x_range[1]:
                ranges_to_remove.append(x_range)
                new_range = [new_range[0], x_range[1]]
            elif new_range[0] < x_range[0] and new_range[1] > x_range[1]:
                ranges_to_remove.append(x_range)
        for x_range in ranges_to_remove:
            self.ranges.remove(x_range)
        if new_range:
            self.ranges.append(new_range)

    def missing_x(self):
        x = None
        if not (self.ranges[0][0] == self.n_min and self.ranges[0][1] == self.n_max):
            if len(self.ranges) == 1:
                if self.ranges[0][0] > self.n_min:
                    x = self.n_min
                else:
                    x = self.n_max
            else:
                x = self.ranges[0][1] + 1
        return x


def main(input_file_name, n_min, n_max):
    with open(input_file_name) as input_file:
        lines = [line.strip() for line in input_file.readlines() if line != '\n']

    rows = [Row(y, n_min, n_max) for y in range(n_min, n_max + 1)]
    for sensor in lines:
        [s_x, s_y, b_x, b_y] = [int(n) for n in re.findall(r'-?\d+\.?\d*', sensor)]
        b_dist = abs(s_x - b_x) + abs(s_y - b_y)
        for y in range(s_y - b_dist, s_y + b_dist + 1):
            if n_min <= y <= n_max:
                y_dist = abs(s_y - y)
                x_dist = b_dist - y_dist
                rows[y].add_range(s_x - x_dist, s_x + x_dist)

    for y, row in enumerate(rows):
        if row.missing_x():
            return row.missing_x() * 4000000 + y


if __name__ == '__main__':
    print(main('test.txt', 0, 20))
    print(main('input.txt', 0, 4000000))
