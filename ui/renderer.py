# renderer.py

import pygame
from ui.assets import BACKGROUND_COLOR, MARGIN_COLOR, TILE_COLORS, DEFAULT_TILE_COLOR, SCREEN_WIDTH
from core.game import Game
from core.tile import Tile
from typing import List

class Renderer:
    def __init__(self, screen : pygame.Surface, font, game: Game):
        self.screen = screen
        self.font = font
        self.game = game

    def draw_board(self, tiles: List[List[Tile]], score: int):
        self.screen.fill(BACKGROUND_COLOR)

        # Draw Title
        title_font = pygame.font.SysFont("monospace", 72, bold=True)
        title_surface = title_font.render("2048", True, (50, 50, 50))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        self.screen.blit(title_surface, title_rect)

        # Draw Score Box
        box_width, box_height = 180, 100
        box_x = self.game.rect.right - box_width
        box_y = self.game.rect.top - box_height - 20
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, MARGIN_COLOR, box_rect, border_radius=12)

        score_label = self.font.render("Score", True, (255, 255, 255))
        score_label_rect = score_label.get_rect(center=(box_rect.centerx, box_rect.top + 25))
        self.screen.blit(score_label, score_label_rect)

        score_value = self.font.render(str(score), True, (255, 255, 255))
        score_value_rect = score_value.get_rect(center=(box_rect.centerx, box_rect.bottom - 25))
        self.screen.blit(score_value, score_value_rect)

        # Draw Game Board
        pygame.draw.rect(self.screen, MARGIN_COLOR, self.game.rect, border_radius=20)
        for row in tiles:
            for tile in row:
                bg_color, fg_color = TILE_COLORS.get(tile.value, DEFAULT_TILE_COLOR)
                pygame.draw.rect(self.screen, bg_color, tile.rect, border_radius=15)
                pygame.draw.rect(self.screen, MARGIN_COLOR, tile.rect, 8, border_radius=15)
                if tile.value != 0:
                    text = self.font.render(str(tile.value), True, fg_color)
                    rect = text.get_rect(center=tile.rect.center)
                    self.screen.blit(text, rect)
