import pygame
from constants import (
    TILE_SIZE,
    TILE_COLOR,
    GRID_COLOR,
    TEXT_COLOR_LIGHT,
    TEXT_COLOR_DARK,
)

game_font = None


class Tile:
    """Represents both logical grid tiles and temporary animated tiles."""

    def __init__(self, x: int, y: int, value: int = 0):
        # logical grid position
        self.value = int(value)
        self.pos = pygame.Vector2(x, y)

        # pixel position for rendering
        self.pixel_pos = pygame.Vector2(
            self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE + TILE_SIZE
        )

        # animation parameters
        self.start_pos = self.pixel_pos.copy()
        self.target_pos = self.pixel_pos.copy()
        self.move_time = 0.0
        self.move_elapsed = 0.0
        self.moving = False

        self.scale = 1.0
        self.start_scale = 1.0
        self.target_scale = 1.0
        self.scale_time = 0.0
        self.scale_elapsed = 0.0
        self.scaling = False

        # visibility flag (used when animation overlays a cell)
        self.visible = True

        # attributes used only for temporary moving tiles
        self.temp = False
        self.merge = False
        self.target_cell = None

    def start_move(self, start_cell, end_cell, duration=0.1, merge=False):
        self.temp = True
        self.merge = merge
        self.target_cell = pygame.Vector2(end_cell)
        self.pixel_pos = pygame.Vector2(
            start_cell[0] * TILE_SIZE, start_cell[1] * TILE_SIZE + TILE_SIZE
        )
        self.start_pos = self.pixel_pos.copy()
        self.target_pos = pygame.Vector2(
            end_cell[0] * TILE_SIZE, end_cell[1] * TILE_SIZE + TILE_SIZE
        )
        self.move_time = duration
        self.move_elapsed = 0.0
        self.moving = True

    def start_scale(self, from_scale, to_scale, duration=0.1):
        self.scale = from_scale
        self.start_scale = from_scale
        self.target_scale = to_scale
        self.scale_time = duration
        self.scale_elapsed = 0.0
        self.scaling = True

    def update(self, dt):
        if self.moving:
            self.move_elapsed += dt
            if self.move_time > 0:
                t = min(self.move_elapsed / self.move_time, 1)
            else:
                t = 1
            self.pixel_pos = self.start_pos.lerp(self.target_pos, t)
            if t >= 1:
                self.moving = False

        if self.scaling:
            self.scale_elapsed += dt
            if self.scale_time > 0:
                t = min(self.scale_elapsed / self.scale_time, 1)
            else:
                t = 1
            self.scale = self.start_scale + (self.target_scale - self.start_scale) * t
            if t >= 1:
                self.scaling = False

    def draw(self, screen):
        if not self.visible:
            return

        rect = pygame.Rect(
            self.pixel_pos.x,
            self.pixel_pos.y,
            TILE_SIZE,
            TILE_SIZE,
        )
        if self.scale != 1:
            rect = rect.inflate(TILE_SIZE * (self.scale - 1), TILE_SIZE * (self.scale - 1))
            rect.center = (
                self.pixel_pos.x + TILE_SIZE / 2,
                self.pixel_pos.y + TILE_SIZE / 2,
            )

        color = TILE_COLOR[self.value]
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, GRID_COLOR, rect, 12)

        if self.value != 0:
            text = game_font.render(
                f"{self.value}",
                True,
                TEXT_COLOR_LIGHT if self.value >= 8 else TEXT_COLOR_DARK,
            )
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

