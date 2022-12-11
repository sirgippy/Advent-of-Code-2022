def new_elf():
    return {'food': [], 'calories': 0}


with open('input.txt') as input_file:
    lines = input_file.readlines()

elves = []
elf = new_elf()
for line in lines:
    if line.strip() == '':
        elves.append(elf)
        elf = new_elf()
    else:
        elf['food'].append(int(line.strip()))
        elf['calories'] += int(line.strip())

elves = sorted(elves, key=lambda e: e['calories'], reverse=True)

print(elves[0]['calories'])
print(elves[0]['calories'] + elves[1]['calories'] + elves[2]['calories'])
