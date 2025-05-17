import random
from copy import deepcopy

class ChessAI:
    def __init__(self, max_depth=3):
        self.max_depth = max_depth
        self.piece_values = {
            'pawn': 100,
            'knight': 320,
            'bishop': 330,
            'rook': 500,
            'queen': 900,
            'king': 20000
        }
        
    def get_best_move(self, board):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # Get all possible moves for black pieces
        possible_moves = self._get_all_moves(board, 'black')
        random.shuffle(possible_moves)  # Add some randomness to make it less predictable
        
        for move in possible_moves:
            # Make move
            temp_board = deepcopy(board)
            temp_board.make_move(move[0], move[1])
            
            # Evaluate move
            score = self._minimax(temp_board, self.max_depth - 1, alpha, beta, False)
            
            if score > best_score:
                best_score = score
                best_move = move
                
            alpha = max(alpha, best_score)
            
        return best_move
    
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
        else:
            min_eval = float('inf')
            for move in self._get_all_moves(board, 'white'):
                temp_board = deepcopy(board)
                temp_board.make_move(move[0], move[1])
                eval = self._minimax(temp_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    
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
        
        # Position evaluation (simple center control)
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        for row, col in center_squares:
            piece = board.get_piece(row, col)
            if piece:
                if piece.color == 'white':
                    score += 10
                else:
                    score -= 10
        
        return score
    
    def _get_all_moves(self, board, color):
        moves = []
        for start_row in range(8):
            for start_col in range(8):
                piece = board.get_piece(start_row, start_col)
                if piece and piece.color == color:
                    for end_row in range(8):
                        for end_col in range(8):
                            if board.is_valid_move((start_row, start_col), (end_row, end_col)):
                                moves.append(((start_row, start_col), (end_row, end_col)))
        return moves 