# Dice Game

A simple command-line dice rolling game implemented in Python.

## Description

This Dice Game is a fun and interactive command-line application where players can roll a virtual six-sided die. The game continues as long as the player wishes to roll again, providing a simple yet entertaining experience.

## Features

- Simulates rolling a six-sided die
- Displays the result of each roll
- Allows players to roll multiple times
- Simple and user-friendly command-line interface

## Requirements

- Python 3.x

## Installation

1. Clone this repository or download the `rolling_dice.py` file.
2. Ensure you have Python 3.x installed on your system.

## How to Play

1. Open a terminal or command prompt.
2. Navigate to the directory containing the `rolling_dice.py` file.
3. Run the game using Python:
   ```
   python rolling_dice.py
   ```
4. Follow the on-screen prompts to roll the dice and play again.

## Game Rules

1. When you start the game, it will automatically roll a die for you and show the result.
2. After each roll, you'll be asked if you want to play again.
3. Enter 'Yes' or 'yes' to roll again, or 'No' or 'no' to end the game.
4. If you enter an invalid input, the game will prompt you to enter a valid response.

## Code Structure

- `roll_dice()`: This function handles the user input for playing again and validates the input.
- `__main__`: The main game loop that initiates the game, rolls the dice, and manages the game flow.
