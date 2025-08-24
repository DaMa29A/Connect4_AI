import pygame

# Dimensioni
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2.5)
WIDTH = 7 * SQUARESIZE
HEIGHT = (6 + 1) * SQUARESIZE
SIZE = (WIDTH, HEIGHT)

# Colori
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Font
pygame.font.init()
FONT = pygame.font.SysFont("monospace", 50)
