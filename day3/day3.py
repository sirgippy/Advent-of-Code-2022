def get_duplicate(rucksack):
    compartment1 = rucksack[:int(len(rucksack) / 2)]
    compartment2 = rucksack[int(len(rucksack) / 2):]

    for item in compartment1:
        if item in compartment2:
            return item


def get_badge(rucksacks):
    for item in rucksacks[0]:
        if item in rucksacks[1]:
            if item in rucksacks[2]:
                return item


def priority(item):
    return ord(item) - 96 if ord(item) >= 97 else ord(item) - 38


with open('input.txt') as input_file:
    rucksacks = input_file.readlines()

print(sum([priority(get_duplicate(rucksack.strip())) for rucksack in rucksacks]))
print(sum([priority(get_badge(rucksacks[pos:pos + 3])) for pos in range(0, len(rucksacks), 3)]))
