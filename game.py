import random
import pygame
from constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, LOGO_SIZE, SCORE_SIZE, TEXT_COLOR_LIGHT, TEXT_COLOR_DARK, GRID_COLOR, BACKGROUND_COLOR, TILE_COLOR
from tile import Tile

logo_font = None
score_font = None

game_font = None  # imported from tile module, but keep variable name for compatibility

class   Game:
    def __init__(self):
        self.score = 0
        self.running = True
        self.tiles = [[Tile(x, y) for y in range(4)] for x in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].pos = pygame.Vector2(i, j)

    def render(self, screen):
        screen.fill(BACKGROUND_COLOR)

        logo_text = logo_font.render("2048", True, TEXT_COLOR_LIGHT)
        logo_rect = logo_text.get_rect(centerx=TILE_SIZE, centery=TILE_SIZE / 2)

        score_text = score_font.render(f"Score: {self.score}", True, TEXT_COLOR_LIGHT)
        score_rect = score_text.get_rect(centerx=SCREEN_WIDTH * 3 / 4, centery=TILE_SIZE / 2)

        pygame.draw.rect(screen, TILE_COLOR[2048], logo_rect.inflate(TILE_SIZE / 4, TILE_SIZE / 8), border_radius=10)
        pygame.draw.rect(screen, TILE_COLOR[2048], score_rect.inflate(TILE_SIZE / 8, TILE_SIZE / 16), border_radius=10)
        screen.blit(logo_text, logo_rect)
        screen.blit(score_text, score_rect)

        for i in range(4):
            for j in range(4):
                self.tiles[i][j].draw(screen)


def is_game_over(game):
    for x in range(4):
        for y in range(4):
            val = game.tiles[x][y].value
            if val == 0:
                return False
            for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < 4 and 0 <= ny < 4:
                    if game.tiles[nx][ny].value == val:
                        return False
    return True

def put_random_tile(game):
    random.seed()
    score = (2,) * 9 + (4,)
    empty = [(x, y) for x in range(4) for y in range(4) if game.tiles[x][y].value == 0]
    if not empty:
        return
    x, y = random.choice(empty)
    game.tiles[x][y].value = random.choice(score)

def     start_game(game):
    game.score = 0
    for x in range(4):
        for y in range(4):
            game.tiles[x][y].value = 0
    for i in range(2):
        put_random_tile(game)

def render_game_over(screen):

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill((238, 228, 218))
    overlay.set_alpha(230)
    screen.blit(overlay, (0, 0))

    game_over_text = logo_font.render("Game Over!", True, TEXT_COLOR_DARK)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(game_over_text, text_rect)

