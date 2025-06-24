import pygame
from ui.assets import TILE_SIZE

class Tile:
    def __init__(self, x, y, offset_x=0, offset_y=0):
        self.value = 0
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(offset_x + x * TILE_SIZE,
                                offset_y + y * TILE_SIZE,
                                TILE_SIZE,
                                TILE_SIZE)
