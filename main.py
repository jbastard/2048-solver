import random
import pygame
import event

TILE_SIZE       = 200
SCREEN_WIDTH    = 4 * TILE_SIZE
SCREEN_HEIGHT   = 5 * TILE_SIZE
FPS             = 60
LOGO_SIZE       = int(TILE_SIZE / 2)
SCORE_SIZE      = int(TILE_SIZE / 5)

TEXT_COLOR_LIGHT = (249, 246, 242)
TEXT_COLOR_DARK = (119, 110, 101)

GRID_COLOR = (187, 173, 160)
BACKGROUND_COLOR = (205, 193, 180)

TILE_COLOR = {
    0:    BACKGROUND_COLOR,
    2:    (238, 228, 218),
    4:    (237, 224, 200),
    8:    (242, 177, 121),
    16:   (245, 149, 99),
    32:   (246, 124, 95),
    64:   (246, 94, 59),
    128:  (237, 207, 114),
    256:  (237, 204, 97),
    512:  (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}


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

if __name__ == '__main__':
    pygame.init()

    game_font = pygame.font.SysFont("monospace", int(TILE_SIZE / 4), bold=True)
    logo_font = pygame.font.SysFont("monospace", LOGO_SIZE, bold=True)
    score_font = pygame.font.SysFont("monospace", SCORE_SIZE, bold=True)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    dt = 0

    game = Game()
    start_game(game)
    while game.running:
        event.handle_events(game, pygame.event.get())
        game.render(screen)
        if is_game_over(game):
            render_game_over(screen)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
    pygame.quit()