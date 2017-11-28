import pygame

FIELD_HEIGHT = 480
FIELD_WIDTH = 800

FPS = 60
TICK_SECOND = 1000 / FPS / 1000
'''One second = 1000 millisecond; 60 frames;'''

# Colors
WHITE = pygame.Color('white')#(255, 255, 255)
BLACK = pygame.Color('black')

PLAYER1 = 1
PLAYER2 = 2
PLAYER_LEFT = PLAYER1
PLAYER_RIGHT = PLAYER2

PLAYER_MARGIN = 32  # How many pixels the players should spawn from their base
