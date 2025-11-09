import pygame
import numpy as np
from configs.gui_config import *
from configs.env_config import ROWS_COUNT, COLUMNS_COUNT

class Connect4GUIRenderer:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        self.rows = ROWS_COUNT
        self.cols = COLUMNS_COUNT
        
        self.width = self.cols * SQUARE_SIZE
        self.height = (self.rows + 1) * SQUARE_SIZE
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Connect 4")

        self.win_font = pygame.font.SysFont("Arial", 40, bold=True)
        
        self.clear_top_bar()
        empty_board = np.zeros((self.rows, self.cols), dtype=np.int8)
        self.draw_board(empty_board)

    def clear_top_bar(self):
        top_area = pygame.Rect(0, 0, self.width, OFFSET_TOP)
        self.screen.fill(COLOR_LIGHT_BLUE, top_area)
        pygame.display.update(top_area)

    def draw_board(self, board):
        board_area = pygame.Rect(0, OFFSET_TOP, self.width, self.height - OFFSET_TOP)
        self.screen.fill(COLOR_LIGHT_BLUE, board_area)

        for r in range(self.rows):
            for c in range(self.cols):
                rect_coords = (c * SQUARE_SIZE, (r + 1) * SQUARE_SIZE, 
                               SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, COLOR_BLUE, rect_coords)
                
                piece_color = COLOR_LIGHT_BLUE # Empty
                if board[r, c] == 1:
                    piece_color = COLOR_RED
                elif board[r, c] == -1:
                    piece_color = COLOR_YELLOW
                
                center_x = int(c * SQUARE_SIZE + SQUARE_SIZE / 2)
                center_y = int((r + 1) * SQUARE_SIZE + SQUARE_SIZE / 2)
                pygame.draw.circle(self.screen, piece_color, (center_x, center_y), RADIUS)
        
        pygame.display.update(board_area)

    def draw_hover_highlight(self, col, is_valid):
        if col < 0: return
            
        highlight_rect = pygame.Rect(
            col * SQUARE_SIZE, OFFSET_TOP, 
            SQUARE_SIZE, self.rows * SQUARE_SIZE
        )
        
        highlight_surface = pygame.Surface((highlight_rect.width, highlight_rect.height), pygame.SRCALPHA)
        
        if is_valid:
            highlight_surface.fill(COLOR_HIGHLIGHT)
        else:
            highlight_surface.fill((255, 0, 0, 75)) # Red
        
        self.screen.blit(highlight_surface, highlight_rect.topleft)
        pygame.display.update(highlight_rect)

    def get_col_from_mouse(self, pos):
        x, y = pos
        if y < OFFSET_TOP: return -1 
        col = x // SQUARE_SIZE
        return col if 0 <= col < self.cols else -1

    def draw_winner_text(self, winner_key, players):
        if winner_key == 0:
            message = "Pareggio!"
            text_color = (50, 50, 50)
        elif winner_key == 1:
            message = f"{players[1].getName()} vince!"
            text_color = COLOR_RED
        else:
            message = f"{players[-1].getName()} vince!"
            text_color = COLOR_YELLOW

        self.clear_top_bar()
        text_surface = self.win_font.render(message, True, text_color)
        text_rect = text_surface.get_rect(
            center=(self.width / 2, OFFSET_TOP / 2) 
        )
        self.screen.blit(text_surface, text_rect)
        pygame.display.update(pygame.Rect(0, 0, self.width, OFFSET_TOP))

    def close(self):
        pygame.display.quit()
        pygame.quit()