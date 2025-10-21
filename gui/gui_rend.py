import pygame
import numpy as np
from configs.gui_config import *
from configs.env_config import ROWS_COUNT, COLUMNS_COUNT

# In Connect4Env.py
def render_gui(screen, board):
    screen.fill(BLUE)

    for r in range(ROWS_COUNT):
        for c in range(COLUMNS_COUNT):
            pos_x = c * SQUARESIZE + SQUARESIZE // 2 # column position
            pos_y = (r * SQUARESIZE) + SQUARESIZE + (SQUARESIZE // 2) # row position

            cell = board[r][c]

            if cell == 1:
                color = RED
            elif cell == -1:
                color = YELLOW
            else:
                color = LIGHT_BLUE

            pygame.draw.circle(screen, color, (pos_x, pos_y), RADIUS)

    pygame.display.update()


# In HumanAgent.py
def check_gui_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            return None
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            x = event.pos[0]
            col = x // SQUARESIZE
            return col

# In play_game.py
def start_gui():
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Connect 4 GUI")
    return screen

# In play_game.py
def show_results(screen, winner):
    label = FONT.render("Draw!" if winner == 0 else f"{'Red' if winner == 1 else 'Yellow'} wins!", 1, RED if winner == 1 else YELLOW)
    screen.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(3000)