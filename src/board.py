class Piece:
    def __init__(self, color, piece_type):
        self.color = color
        self.piece_type = piece_type
        self.has_moved = False

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()
    
    def initialize_board(self):
        # Initialize pawns
        for col in range(8):
            self.board[1][col] = Piece('black', 'pawn')
            self.board[6][col] = Piece('white', 'pawn')
        
        # Initialize other pieces
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col in range(8):
            self.board[0][col] = Piece('black', piece_order[col])
            self.board[7][col] = Piece('white', piece_order[col])
    
    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def is_valid_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.get_piece(start_row, start_col)
        
        if not piece:
            return False
            
        # Basic move validation
        if not (0 <= end_row < 8 and 0 <= end_col < 8):
            return False
            
        target = self.get_piece(end_row, end_col)
        if target and target.color == piece.color:
            return False
            
        # Piece-specific move validation
        if piece.piece_type == 'pawn':
            return self._is_valid_pawn_move(start, end)
        elif piece.piece_type == 'rook':
            return self._is_valid_rook_move(start, end)
        elif piece.piece_type == 'knight':
            return self._is_valid_knight_move(start, end)
        elif piece.piece_type == 'bishop':
            return self._is_valid_bishop_move(start, end)
        elif piece.piece_type == 'queen':
            return self._is_valid_queen_move(start, end)
        elif piece.piece_type == 'king':
            return self._is_valid_king_move(start, end)
            
        return False
    
    def make_move(self, start, end):
        if not self.is_valid_move(start, end):
            return False
            
        start_row, start_col = start
        end_row, end_col = end
        
        self.board[end_row][end_col] = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
        self.board[end_row][end_col].has_moved = True
        
        return True
    
    def _is_valid_pawn_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        piece = self.get_piece(start_row, start_col)
        
        direction = -1 if piece.color == 'white' else 1
        start_pos = 6 if piece.color == 'white' else 1
        
        # Forward move
        if end_col == start_col and end_row == start_row + direction:
            return self.get_piece(end_row, end_col) is None
            
        # Initial two-square move
        if not piece.has_moved and end_col == start_col and end_row == start_row + 2 * direction:
            return (self.get_piece(start_row + direction, start_col) is None and
                   self.get_piece(end_row, end_col) is None)
                   
        # Capture
        if abs(end_col - start_col) == 1 and end_row == start_row + direction:
            target = self.get_piece(end_row, end_col)
            return target is not None and target.color != piece.color
            
        return False
    
    def _is_valid_rook_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        if start_row != end_row and start_col != end_col:
            return False
            
        # Check if path is clear
        if start_row == end_row:
            step = 1 if end_col > start_col else -1
            for col in range(start_col + step, end_col, step):
                if self.get_piece(start_row, col):
                    return False
        else:
            step = 1 if end_row > start_row else -1
            for row in range(start_row + step, end_row, step):
                if self.get_piece(row, start_col):
                    return False
                    
        return True
    
    def _is_valid_knight_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def _is_valid_bishop_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        if abs(end_row - start_row) != abs(end_col - start_col):
            return False
            
        row_step = 1 if end_row > start_row else -1
        col_step = 1 if end_col > start_col else -1
        
        current_row, current_col = start_row + row_step, start_col + col_step
        while current_row != end_row and current_col != end_col:
            if self.get_piece(current_row, current_col):
                return False
            current_row += row_step
            current_col += col_step
            
        return True
    
    def _is_valid_queen_move(self, start, end):
        return (self._is_valid_rook_move(start, end) or 
                self._is_valid_bishop_move(start, end))
    
    def _is_valid_king_move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        row_diff = abs(end_row - start_row)
        col_diff = abs(end_col - start_col)
        
        return row_diff <= 1 and col_diff <= 1 