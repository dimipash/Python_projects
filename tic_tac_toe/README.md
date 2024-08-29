# Tic-Tac-Toe Game

This is a simple implementation of the classic Tic-Tac-Toe game in Python. The game is played automatically by two players, with moves chosen randomly.

## Features

- Automatic gameplay between two players
- Random move selection
- Visual representation of the game board
- Win condition checking for rows, columns, and diagonals

## Requirements

- Python 3.x
- NumPy library

## Installation

1. Clone this repository.

2. Navigate to the project directory:

   ```
   cd tic_tac_toe
   ```

3. Install the required dependencies:
   ```
   pip install numpy
   ```

## Usage

Run the game by executing the Python script:

```
python tictactoe.py
```

The game will automatically play out, displaying the board state after each move and announcing the winner at the end.

## How It Works

1. The game creates an empty 3x3 board.
2. Players take turns making random moves on the board.
3. After each move, the board is displayed and checked for a win condition.
4. The game continues until a player wins or the board is full (resulting in a tie).

## Functions

- `create_board()`: Initializes an empty game board.
- `possibilities(board)`: Finds all empty spaces on the board.
- `random_place(board, player)`: Places a player's mark in a random empty space.
- `row_win(board, player)`: Checks for a win in any row.
- `col_win(board, player)`: Checks for a win in any column.
- `diag_win(board, player)`: Checks for a win in either diagonal.
- `evaluate(board)`: Determines if there's a winner or a tie.
- `play_game()`: Main function to run the game.
