from enum import Enum


class TheirRPS(Enum):
    ROCK = 'A'
    PAPER = 'B'
    SCISSORS = 'C'


class MyRPS(Enum):
    ROCK = 'X'
    PAPER = 'Y'
    SCISSORS = 'Z'


def get_score(their_choice, my_choice):
    score = 0
    if my_choice == MyRPS.ROCK:
        score += 1
        if their_choice == TheirRPS.ROCK:
            score += 3
        elif their_choice == TheirRPS.SCISSORS:
            score += 6
    elif my_choice == MyRPS.PAPER:
        score += 2
        if their_choice == TheirRPS.PAPER:
            score += 3
        elif their_choice == TheirRPS.ROCK:
            score += 6
    else:  # scissors
        score += 3
        if their_choice == TheirRPS.SCISSORS:
            score += 3
        elif their_choice == TheirRPS.PAPER:
            score += 6
    return score


with open('input.txt') as input_file:
    lines = input_file.readlines()

result = 0
for line in lines:
    choices = line.split()
    theirs = TheirRPS(choices[0])
    mine = MyRPS(choices[1])
    result += get_score(theirs, mine)

print(result)
