"""
A simple command-line dice game implementation.

This script simulates a dice game where the user can roll a virtual dice and continue playing as long as they wish. The program generates a random number between 1 and 6, representing the outcome of a dice roll.

Features:
- Random dice roll simulation
- Prompts the user to play again after each roll
- Input validation for the user's choice (Yes/No)
- Continuous gameplay until the user chooses to exit

Requirements:
- Python 3.x

Note: This script does not require any external libraries or dependencies.
"""

import random


def roll_dice():
    print('\nDo you want to play again ?')
    print('Enter Yes/No')
    choice = input()

    if choice == '':
        print('Wrong Input !!! Enter again Yes/No')
        choice = roll_dice()
    return choice


if __name__ == '__main__':
    print('Welcome to the Dice Game !!!')
    dice_value = random.randint(1, 6)
    print('You got ', dice_value)
    choice = roll_dice()

    while choice:
        if choice == 'No' or choice == 'no':
            break
        elif choice == 'Yes' or choice == 'yes':
            dice_value = random.randint(1, 6)
            print('You got ', dice_value)
            choice = roll_dice()
        else:
            print('Wrong Input !!! Enter again Yes/No')
            choice = roll_dice()
