import operator
import re

ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

basic_pattern = r'([a-z]{4}): (\d+)'
math_pattern = r'([a-z]{4}): ([a-z]{4}) (.) ([a-z]{4})'


class Monkey:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def get_value(self):
        return self.value

    def contains_humn(self):
        return self.key == 'humn'

    def determine_humn_value(self, value):
        if self.key == 'humn':
            return value
        else:
            raise ValueError('Not humn. Try again.')


class MathMonkey:
    def __init__(self, child_1, child_2, operation, monkeys):
        self.child_1 = child_1
        self.child_2 = child_2
        self.operation = ops[operation]
        self.monkeys = monkeys

    def get_value(self):
        return self.operation(self.monkeys[self.child_1].get_value(), self.monkeys[self.child_2].get_value())

    def contains_humn(self):
        return self.monkeys[self.child_1].contains_humn() or self.monkeys[self.child_2].contains_humn()

    def determine_humn_value(self, value):
        if self.monkeys[self.child_1].contains_humn():
            if self.operation == operator.add:
                return self.monkeys[self.child_1].determine_humn_value(value - self.monkeys[self.child_2].get_value())
            elif self.operation == operator.sub:
                return self.monkeys[self.child_1].determine_humn_value(value + self.monkeys[self.child_2].get_value())
            elif self.operation == operator.mul:
                return self.monkeys[self.child_1].determine_humn_value(value / self.monkeys[self.child_2].get_value())
            else:
                return self.monkeys[self.child_1].determine_humn_value(value * self.monkeys[self.child_2].get_value())
        else:
            if self.operation == operator.add:
                return self.monkeys[self.child_2].determine_humn_value(value - self.monkeys[self.child_1].get_value())
            elif self.operation == operator.sub:
                return self.monkeys[self.child_2].determine_humn_value(self.monkeys[self.child_1].get_value() - value)
            elif self.operation == operator.mul:
                return self.monkeys[self.child_2].determine_humn_value(value / self.monkeys[self.child_1].get_value())
            else:
                return self.monkeys[self.child_2].determine_humn_value(self.monkeys[self.child_1].get_value() / value)


def main(input_file_name, part1):
    with open(input_file_name) as input_file:
        descriptions = [line.strip() for line in input_file.readlines() if line != '\n']

    monkeys = {}

    for description in descriptions:
        if re.match(basic_pattern, description):
            [monkey, value] = re.match(basic_pattern, description).groups()
            monkeys[monkey] = Monkey(monkey, int(value))
        else:
            [monkey, child_1, operation, child_2] = re.match(math_pattern, description).groups()
            monkeys[monkey] = MathMonkey(child_1, child_2, operation, monkeys)

    if part1:
        return monkeys['root'].get_value()
    else:
        if monkeys[monkeys['root'].child_1].contains_humn():
            return monkeys[monkeys['root'].child_1].determine_humn_value(monkeys[monkeys['root'].child_2].get_value())
        else:
            return monkeys[monkeys['root'].child_2].determine_humn_value(monkeys[monkeys['root'].child_1].get_value())


if __name__ == '__main__':
    print(main('test.txt', True))
    print(main('input.txt', True))
    print(main('test.txt', False))
    print(main('input.txt', False))
