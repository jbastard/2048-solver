import pygame
from ui.assets import TILE_SIZE

class Tile:
    def __init__(self, x, y):
        self.value = 0
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
