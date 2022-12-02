from enum import Enum


class TheirRPS(Enum):
    ROCK = 'A'
    PAPER = 'B'
    SCISSORS = 'C'


class MyRPS(Enum):
    LOSE = 'X'
    DRAW = 'Y'
    WIN = 'Z'


def get_score(their_choice, my_choice):
    score = 0
    if my_choice == MyRPS.LOSE:
        if their_choice == TheirRPS.PAPER:  # I choose Rock
            score += 1
        elif their_choice == TheirRPS.SCISSORS:  # I choose Paper
            score += 2
        else:   # They chose Rock, I chose Scissors
            score += 3
    elif my_choice == MyRPS.DRAW:
        score += 3
        if their_choice == TheirRPS.ROCK:  # I choose Rock
            score += 1
        elif their_choice == TheirRPS.PAPER:  # I choose Paper
            score += 2
        else:  # They chose Scissors, I chose Scissors
            score += 3
    else:  # win
        score += 6
        if their_choice == TheirRPS.SCISSORS:  # I choose Rock
            score += 1
        elif their_choice == TheirRPS.ROCK:  # I choose Paper
            score += 2
        else:  # They chose Paper, I chose Scissors
            score += 3
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
