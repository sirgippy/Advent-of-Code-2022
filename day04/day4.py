def translate_assignment(assignment):
    assignment_pair = assignment.split(',')
    bounds = [assignment.split('-') for assignment in assignment_pair]
    return [range(int(bound[0]), int(bound[1]) + 1) for bound in bounds]


with open('input.txt') as input_file:
    raw_assignments = [line.strip() for line in input_file.readlines()]

list_pairs = [translate_assignment(assignment) for assignment in raw_assignments]

fully_contained = 0
overlap = 0
for pair in list_pairs:
    if all(x in pair[1] for x in pair[0]) or all(x in pair[0] for x in pair[1]):
        fully_contained += 1
    if any(x in pair[1] for x in pair[0]):
        overlap += 1

print(fully_contained)
print(overlap)
