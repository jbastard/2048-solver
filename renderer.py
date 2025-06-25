import pygame
from constants import (
    TILE_SIZE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    LOGO_SIZE,
    SCORE_SIZE,
    TEXT_COLOR_LIGHT,
    TEXT_COLOR_DARK,
    GRID_COLOR,
    BACKGROUND_COLOR,
    TILE_COLOR,
)
from tile import Tile
from game_logic import Game

logo_font = None
score_font = None

game_font = None  # imported from tile module, kept for compatibility


class GameRenderer:
    def __init__(self, game: Game):
        self.game = game
        self.tiles = [[Tile(x, y) for y in range(4)] for x in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].pos = pygame.Vector2(i, j)
                self.tiles[i][j].value = self.game.board[i][j]

        # list of temporary tiles used for movement animations
        self.anim_tiles = []

    def sync_from_logic(self):
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].value = self.game.board[i][j]

    def move(self, dx: int, dy: int):
        operations, new_tile = self.game.move(dx, dy)
        self.sync_from_logic()
        for op in operations:
            sx, sy = op["from"]
            dx_, dy_ = op["to"]
            val = op["value"]
            merge = op["merge"]
            anim = Tile(dx_, dy_, value=val)
            anim.start_move((sx, sy), (dx_, dy_), 0.1, merge=merge)
            self.anim_tiles.append(anim)
            self.tiles[dx_][dy_].visible = False
        if new_tile:
            nx, ny = new_tile
            self.tiles[nx][ny].start_scale(0.0, 1.0, 0.1)

    def update(self, dt):
        # update all tiles for scaling animations
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].update(dt)

        # update temporary moving tiles
        for t in self.anim_tiles[:]:
            t.update(dt)
            if not t.moving:
                dest = self.tiles[int(t.target_cell.x)][int(t.target_cell.y)]
                dest.visible = True
                if t.merge:
                    dest.start_scale(1.2, 1.0, 0.1)
                self.anim_tiles.remove(t)

    def render(self, screen):
        screen.fill(BACKGROUND_COLOR)

        logo_text = logo_font.render("2048", True, TEXT_COLOR_LIGHT)
        logo_rect = logo_text.get_rect(centerx=TILE_SIZE, centery=TILE_SIZE / 2)

        score_text = score_font.render(f"Score: {self.game.score}", True, TEXT_COLOR_LIGHT)
        score_rect = score_text.get_rect(centerx=SCREEN_WIDTH * 3 / 4, centery=TILE_SIZE / 2)

        pygame.draw.rect(screen, TILE_COLOR[2048], logo_rect.inflate(TILE_SIZE / 4, TILE_SIZE / 8), border_radius=10)
        pygame.draw.rect(screen, TILE_COLOR[2048], score_rect.inflate(TILE_SIZE / 8, TILE_SIZE / 16), border_radius=10)
        screen.blit(logo_text, logo_rect)
        screen.blit(score_text, score_rect)

        for i in range(4):
            for j in range(4):
                self.tiles[i][j].draw(screen)

        for t in self.anim_tiles:
            t.draw(screen)


def render_game_over(screen):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((238, 228, 218))
    overlay.set_alpha(230)
    screen.blit(overlay, (0, 0))

    game_over_text = logo_font.render("Game Over!", True, TEXT_COLOR_DARK)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(game_over_text, text_rect)
