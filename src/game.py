import pygame
import sys
import os
from board import Board
from ai import ChessAI

class ChessGame:
    def __init__(self):
        pygame.init()
        self.WINDOW_SIZE = 800
        self.SQUARE_SIZE = self.WINDOW_SIZE // 8
        self.screen = pygame.display.set_mode((self.WINDOW_SIZE, self.WINDOW_SIZE))
        pygame.display.set_caption("Chess AI")
        
        self.board = Board()
        self.ai = ChessAI()
        self.selected_piece = None
        self.player_turn = True  # True for white (player), False for black (AI)
        self.valid_moves = []  # Store valid moves for selected piece
        
        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (128, 128, 128)
        self.HIGHLIGHT = (124, 252, 0, 128)
        self.SELECTED = (255, 255, 0, 128)
        self.VALID_MOVE = (0, 255, 0, 128)  # Green highlight for valid moves
        self.SUGGESTED_MOVE = (0, 0, 255, 128)  # Blue highlight for suggested move
        
        # Load piece images
        self.piece_images = {}
        self.load_piece_images()
        
        # AI suggestion
        self.suggested_move = None
        
    def load_piece_images(self):
        pieces = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        for piece in pieces:
            for color in colors:
                # For now, we'll use text to represent pieces
                self.piece_images[f"{color}_{piece}"] = self.create_text_piece(piece, color)
    
    def create_text_piece(self, piece_type, color):
        # Create a surface for the piece
        surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        
        # Draw a circle background
        pygame.draw.circle(surface, 
                         (255, 255, 255) if color == 'white' else (0, 0, 0),
                         (self.SQUARE_SIZE // 2, self.SQUARE_SIZE // 2),
                         self.SQUARE_SIZE // 3)
        
        # Add piece letter
        font = pygame.font.Font(None, 36)
        text_color = (0, 0, 0) if color == 'white' else (255, 255, 255)
        piece_letter = piece_type[0].upper()
        text = font.render(piece_letter, True, text_color)
        text_rect = text.get_rect(center=(self.SQUARE_SIZE // 2, self.SQUARE_SIZE // 2))
        surface.blit(text, text_rect)
        
        return surface
        
    def get_valid_moves(self, start_pos):
        valid_moves = []
        start_row, start_col = start_pos
        
        for row in range(8):
            for col in range(8):
                if self.board.is_valid_move(start_pos, (row, col)):
                    valid_moves.append((row, col))
        
        return valid_moves
    
    def get_ai_suggestion(self):
        if self.player_turn:
            # Get AI's evaluation of the current position
            best_move = self.ai.get_best_move(self.board)
            if best_move:
                return best_move
        return None
        
    def draw_board(self):
        for row in range(8):
            for col in range(8):
                # Draw square
                color = self.WHITE if (row + col) % 2 == 0 else self.BLACK
                pygame.draw.rect(self.screen, color, 
                               (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                self.SQUARE_SIZE, self.SQUARE_SIZE))
                
                # Draw piece
                piece = self.board.get_piece(row, col)
                if piece:
                    piece_key = f"{piece.color}_{piece.piece_type}"
                    self.screen.blit(self.piece_images[piece_key],
                                   (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                
                # Draw selection highlight
                if self.selected_piece and (row, col) == self.selected_piece:
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill(self.SELECTED)
                    self.screen.blit(s, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                
                # Draw valid moves highlight
                if self.selected_piece and (row, col) in self.valid_moves:
                    s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                    s.fill(self.VALID_MOVE)
                    self.screen.blit(s, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
                
                # Draw suggested move highlight
                if self.suggested_move:
                    start, end = self.suggested_move
                    if (row, col) in [start, end]:
                        s = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                        s.fill(self.SUGGESTED_MOVE)
                        self.screen.blit(s, (col * self.SQUARE_SIZE, row * self.SQUARE_SIZE))
    
    def handle_click(self, pos):
        if not self.player_turn:
            return
            
        col = pos[0] // self.SQUARE_SIZE
        row = pos[1] // self.SQUARE_SIZE
        
        if self.selected_piece is None:
            piece = self.board.get_piece(row, col)
            if piece and piece.color == 'white':
                self.selected_piece = (row, col)
                self.valid_moves = self.get_valid_moves(self.selected_piece)
        else:
            if (row, col) in self.valid_moves:
                if self.board.make_move(self.selected_piece, (row, col)):
                    self.player_turn = False
            self.selected_piece = None
            self.valid_moves = []
    
    def run(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_h:  # Press 'h' for hint
                        self.suggested_move = self.get_ai_suggestion()
            
            if not self.player_turn:
                ai_move = self.ai.get_best_move(self.board)
                if ai_move:
                    self.board.make_move(ai_move[0], ai_move[1])
                self.player_turn = True
                self.suggested_move = None  # Clear suggestion after AI move
            
            self.draw_board()
            pygame.display.flip()
            clock.tick(60)  # Limit to 60 FPS

if __name__ == "__main__":
    game = ChessGame()
    game.run() 