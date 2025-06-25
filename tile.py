import pygame
from constants import TILE_SIZE, TILE_COLOR, GRID_COLOR, TEXT_COLOR_LIGHT, TEXT_COLOR_DARK

game_font = None

class   Tile:
    def __init__(self, x, y):
        self.value = int(0)
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE + TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.text = None

    def draw(self, screen):
        color = TILE_COLOR[self.value]
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, GRID_COLOR, self.rect, 12)
        self.text = game_font.render(f"{self.value}", True, TEXT_COLOR_LIGHT if self.value >= 8 else TEXT_COLOR_DARK)
        text_rect = self.text.get_rect(center=self.rect.center)
        if self.value != 0:
            screen.blit(self.text, text_rect)
