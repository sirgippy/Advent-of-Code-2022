from math import ceil, log

from_snafu = {
    '2': 2,
    '1': 1,
    '0': 0,
    '-': -1,
    '=': -2
}

to_snafu = {
    2: '2',
    1: '1',
    0: '0',
    -1: '-',
    -2: '='
}


def main(input_file_name):
    with open(input_file_name) as input_file:
        snafu_numbers = [line.strip() for line in input_file.readlines() if line != '\n']

    fuel_needed = 0
    for number in snafu_numbers:
        fuel_needed += sum(
            [from_snafu[digit] * 5 ** place for digit, place in zip(number, range(len(number) - 1, -1, -1))]
        )

    n = ceil(log(fuel_needed, 5) - log(2.5, 5))

    snafu_needed = ''
    remaining = fuel_needed
    for i in range(n, -1, -1):
        digit = round(remaining / 5 ** i)
        snafu_needed += to_snafu[digit]
        remaining -= digit * 5 ** i

    return snafu_needed


if __name__ == '__main__':
    print(main('test.txt'))
    print(main('input.txt'))
