# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    renderer.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cpoulain <cpoulain@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/25 17:20:33 by cpoulain          #+#    #+#              #
#    Updated: 2025/06/26 11:17:53 by cpoulain         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pygame
from ui.assets import BACKGROUND_COLOR, MARGIN_COLOR, TILE_COLORS, DEFAULT_TILE_COLOR, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE
from core.game import Game
from core.tile import Tile
from ui.tile_animator import TileAnimator
from typing import List

class Renderer:
    def __init__(self, screen : pygame.Surface, font, game: Game, animator: TileAnimator):
        self.screen = screen
        self.font = font
        self.game = game
        self.animator = animator

    def draw_board(self, tiles: List[List[Tile]], score: int):
        self.animator.update_animations()
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
                if tile.value == 0:
                    continue

                bg_color, fg_color = TILE_COLORS.get(tile.value, DEFAULT_TILE_COLOR)

                draw_pos = tile.screen_pos if tile.animating else pygame.Vector2(tile.rect.topleft)
                tile_rect = pygame.Rect(draw_pos, (TILE_SIZE, TILE_SIZE))
                tile_rect.width = tile_rect.height = TILE_SIZE * tile.scale
                tile_rect.center = (draw_pos.x + TILE_SIZE // 2, draw_pos.y + TILE_SIZE // 2)

                pygame.draw.rect(self.screen, bg_color, tile_rect, border_radius=15)
                pygame.draw.rect(self.screen, MARGIN_COLOR, tile_rect, 8, border_radius=15)

                text = self.font.render(str(tile.value), True, fg_color)
                text_rect = text.get_rect(center=tile_rect.center)
                self.screen.blit(text, text_rect)

        if self.game.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            over_text = self.font.render("Game Over", True, (255, 255, 255))
            over_rect = over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            hint_text = self.font.render("Press R to restart", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(over_text, over_rect)
            self.screen.blit(hint_text, hint_rect)

        if self.game.confirm_restart:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            prompt = self.font.render("Restart? Y/N", True, (255, 255, 255))
            prompt_rect = prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + (100 if self.game.game_over else 0)))
            self.screen.blit(prompt, prompt_rect)

