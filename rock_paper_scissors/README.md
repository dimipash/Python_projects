# Rock, Paper, Scissors Game

A simple command-line implementation of the classic Rock, Paper, Scissors game in Python.

## Description

This Python script allows users to play Rock, Paper, Scissors against a computer opponent. The game features a clean interface, input validation, and the option to play multiple rounds.

## Features

- Command-line interface
- Random computer opponent choices
- Input validation for user choices
- Option to play multiple rounds
- Clear screen functionality for better readability

## Requirements

- Python 3.x

## Installation

1. Clone this repository or download the script.
2. Ensure you have Python 3.x installed on your system.

## Usage

Run the script using Python:

```
python rock_paper_scissors.py
```

Follow the on-screen prompts to play the game:

1. Choose your weapon by entering 'R' for Rock, 'P' for Paper, or 'S' for Scissors.
2. The computer will randomly select its choice.
3. The winner of the round will be displayed.
4. You'll be asked if you want to play again.

## How to Play

- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
- If both players choose the same option, it's a tie

## Code Structure

- `check_play_status()`: Handles the logic for asking the user if they want to play again.
- `play_rps()`: The main game loop that handles user input, computer choice, and determines the winner.
- `if __name__ == "__main__":`: Ensures the game is only played when the script is run directly.
