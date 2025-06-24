# renderer.py

import pygame
from ui.assets import BACKGROUND_COLOR, MARGIN_COLOR, TILE_COLORS, DEFAULT_TILE_COLOR
from core.game import Game

class Renderer:
    def __init__(self, screen : pygame.Surface, font, game: Game):
        self.screen = screen
        self.font = font
        self.game = game

    def draw_board(self, tiles):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, MARGIN_COLOR, self.game.rect, border_radius=20)
        for row in tiles:
            for tile in row:
                color = TILE_COLORS.get(tile.value, DEFAULT_TILE_COLOR)
                pygame.draw.rect(self.screen, MARGIN_COLOR, tile.rect, 8)
                pygame.draw.rect(self.screen, color, tile.rect, border_radius=15)
                pygame.draw.rect(self.screen, MARGIN_COLOR, tile.rect, 8, border_radius=15)
                if tile.value != 0:
                    text = self.font.render(f"{tile.value}", True, (255, 0, 0))
                    rect = text.get_rect(center=tile.rect.center)
                    self.screen.blit(text, rect)
