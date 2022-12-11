from math import floor
import re
from copy import deepcopy

with open('input.txt') as input_file:
    initial_position = {}
    reading_initial_position = True
    while reading_initial_position:
        line = input_file.readline().strip()
        if line[0] != '1':
            done_with_row = False
            idx = 1
            while not done_with_row:
                if idx > len(line):
                    done_with_row = True
                else:
                    this_item = line[idx]
                    column = floor(idx / 4) + 1
                    if this_item == ' ':
                        pass
                    elif column in initial_position.keys():
                        initial_position[column].append(this_item)
                    else:
                        initial_position[column] = [this_item]
                    idx += 4
        else:
            reading_initial_position = False
            _ = input_file.readline()
    position_a = {key: value[::-1] for key, value in initial_position.items()}
    position_b = deepcopy(position_a)

    while True:
        line = input_file.readline()
        if not line:
            break
        else:
            (items, move_from, move_to) = re.findall('\d+', line)
            b_queue = []
            for _ in range(int(items)):
                position_a[int(move_to)].append(position_a[int(move_from)].pop())
                b_queue.append(position_b[int(move_from)].pop())
            for _ in range(len(b_queue)):
                position_b[int(move_to)].append(b_queue.pop())

answer_a = []
answer_b = []
for i in range(1, max(position_a.keys()) + 1):
    answer_a.append(position_a[i].pop())
    answer_b.append(position_b[i].pop())

print(answer_a)
print(answer_b)
