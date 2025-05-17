# Intelligent Chess Agent with Pygame

## Christopher Mireles

## Problem Statement

The goal of this project is to create an intelligent chess-playing agent that can compete against human players. The implementation focuses on creating a complete chess game with a graphical interface and an AI opponent that uses advanced game theory algorithms to make strategic decisions.

## Approach

The project implements several key components:

1. **Board Representation**

   - 8x8 grid representation using a 2D array
   - Piece objects with color and type attributes
   - Move validation for all chess pieces

2. **AI Implementation**

   - Minimax algorithm with alpha-beta pruning
   - Depth-limited search (default depth: 3)
   - Evaluation function considering:
     - Material value (piece values)
     - Positional control (center control)
     - Move validation and legal move generation

3. **User Interface**
   - Pygame-based graphical interface
   - Interactive piece movement
   - Visual feedback for:
     - Selected pieces
     - Valid moves
     - AI suggestions

## Software Components

### Architecture Diagram

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Game UI      │     │    Board        │     │      AI         │
│  (Pygame)       │◄────┤  (Game Logic)   │◄────┤  (Minimax)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  User Input     │     │ Move Validation │     │ Move Generation │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Key Components

1. **Game UI (game.py)**

   - Handles user interaction
   - Renders the chess board and pieces
   - Manages game state and turn-based play
   - Implements move highlighting and suggestions

2. **Board Logic (board.py)**

   - Manages piece placement and movement
   - Implements chess rules and move validation
   - Tracks game state and piece positions

3. **AI Engine (ai.py)**
   - Implements minimax algorithm with alpha-beta pruning
   - Evaluates board positions
   - Generates and selects optimal moves

## Technical Implementation

### Programming Language and Libraries

- **Python 3.12**
- **Pygame 2.6.1**: For graphical interface and user interaction
- **NumPy 2.2.5**: For efficient array operations (planned for future optimization)

### Key Algorithms

1. **Minimax with Alpha-Beta Pruning**

```python
def _minimax(self, board, depth, alpha, beta, maximizing_player):
    if depth == 0:
        return self._evaluate_board(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in self._get_all_moves(board, 'black'):
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            eval = self._minimax(temp_board, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
```

2. **Board Evaluation Function**

```python
def _evaluate_board(self, board):
    score = 0
    # Material evaluation
    for row in range(8):
        for col in range(8):
            piece = board.get_piece(row, col)
            if piece:
                value = self.piece_values[piece.piece_type]
                if piece.color == 'white':
                    score += value
                else:
                    score -= value
    return score
```

## Evaluation

### Performance Metrics

1. **AI Strength**

   - Search depth: 3 moves ahead
   - Average move calculation time: < 1 second
   - Evaluation considers material and position

2. **User Experience**
   - Interactive piece selection
   - Visual move validation
   - AI move suggestions (press 'h' for hint)

### Limitations

1. Current implementation doesn't include:
   - Castling
   - En passant
   - Pawn promotion
   - Check/checkmate detection

## Conclusion and Future Work

### Lessons Learned

1. Importance of efficient board representation
2. Balance between AI strength and response time
3. Value of user feedback in game development

### Future Improvements

1. **AI Enhancements**

   - Implement deeper search with iterative deepening
   - Add opening book database
   - Improve evaluation function with more positional factors

2. **Game Features**

   - Add special moves (castling, en passant)
   - Implement check/checkmate detection
   - Add move history and undo functionality
   - Include proper piece images

3. **Performance Optimization**
   - Utilize NumPy for faster board operations
   - Implement move caching
   - Optimize move generation

## References

1. Pygame Documentation: https://www.pygame.org/docs/
2. Chess Programming Wiki: https://www.chessprogramming.org/
3. Python Documentation: https://docs.python.org/3/

## Code Organization

```
chess_ai/
├── src/
│   ├── game.py      # Main game interface and UI
│   ├── board.py     # Board representation and move validation
│   └── ai.py        # AI implementation with minimax
├── assets/
│   └── pieces/      # Directory for piece images (future)
├── requirements.txt # Project dependencies
└── README.md       # Setup and usage instructions
```

## Setup and Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the game:
   ```bash
   python src/game.py
   ```
3. Controls:
   - Click to select and move pieces
   - Press 'h' for AI move suggestion
   - Close window to exit
