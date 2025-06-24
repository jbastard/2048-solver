# renderer.py

import pygame
from ui.assets import BACKGROUND_COLOR

class Renderer:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font

    def draw_board(self, tiles):
        for row in tiles:
            for tile in row:
                pygame.draw.rect(self.screen, BACKGROUND_COLOR, tile.rect)
                pygame.draw.rect(self.screen, (0, 0, 255), tile.rect, 16)
                if tile.value != 0:
                    text = self.font.render(f"{tile.value}", True, (255, 0, 0))
                    rect = text.get_rect(center=tile.rect.center)
                    self.screen.blit(text, rect)
