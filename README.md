# Chess AI

A chess game with an AI opponent implemented in Python using Pygame. The AI uses the minimax algorithm with alpha-beta pruning to make intelligent moves.

## Features

- Complete chess game implementation
- AI opponent using minimax algorithm with alpha-beta pruning
- Material and positional evaluation
- Simple graphical interface using Pygame

## Requirements

- Python 3.7+
- Pygame
- NumPy

## Installation

1. Clone the repository
2. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the game:

```bash
python src/game.py
```

### Controls

- Click on a piece to select it
- Click on a valid destination square to move the piece
- The AI will automatically make its move after you complete yours

## Implementation Details

- The game uses a standard 8x8 chess board representation
- The AI evaluates positions based on:
  - Material value (piece values)
  - Center control
- The AI uses minimax with alpha-beta pruning to a depth of 3 moves

## Future Improvements

- Add piece images instead of simple shapes
- Implement castling and en passant
- Add move history and undo functionality
- Improve AI evaluation function
- Add difficulty levels
