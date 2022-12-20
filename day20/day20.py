class Number:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def get_right(self, distance, chain_length):
        target = self
        for _ in range(distance % chain_length):
            target = target.right
        return target

    def get_left(self, distance, chain_length):
        target = self
        for _ in range(distance % chain_length):
            target = target.left
        return target

    def jump_right(self, distance, chain_length):
        self.left.right = self.right
        self.right.left = self.left

        target = self.get_right(distance, chain_length)

        self.right = target.right
        self.left = target

        target.right = self
        self.right.left = self

    def jump_left(self, distance, chain_length):
        self.left.right = self.right
        self.right.left = self.left

        target = self.get_left(distance, chain_length)

        self.left = target.left
        self.right = target

        target.left = self
        self.left.right = self


def main(input_file_name, key, rounds):
    with open(input_file_name) as input_file:
        numbers = [int(line.strip()) * key for line in input_file.readlines() if line != '\n']

    process_order = []
    prev = None
    first = None
    zero = None
    for i, value in enumerate(numbers):
        number = Number(value)
        if i == 0:
            first = number
        else:
            number.left = prev
            prev.right = number
        if value == 0:
            zero = number
        process_order.append(number)
        prev = number
    first.left = prev
    prev.right = first

    for i in range(rounds):
        for number in process_order:
            if number.value > 0:
                number.jump_right(number.value, len(numbers) - 1)
            elif number.value < 0:
                number.jump_left(-number.value, len(numbers) - 1)

    return sum([zero.get_right(1000 * i, len(numbers)).value for i in range(1, 4)])


if __name__ == '__main__':
    print(main('test.txt', 1, 1))
    print(main('input.txt', 1, 1))
    print(main('test.txt', 811589153, 10))
    print(main('input.txt', 811589153, 10))
