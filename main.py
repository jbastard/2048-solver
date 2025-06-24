import random
import pygame
import event

TILE_SIZE       = 200
SCREEN_WIDTH    = 800
SCREEN_HEIGHT   = 800
FPS             = 60

BACKGROUND_COLOR = (255, 222, 173)


class   Tile:
    def __init__(self, x, y):
        self.value = int(0)
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(self.pos.x * TILE_SIZE, self.pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.text = None

    def draw(self, screen):
        pygame.draw.rect(screen, BACKGROUND_COLOR, self.rect)
        pygame.draw.rect(screen, (0, 0, 255), self.rect, 16)
        self.text = font.render(f"{self.value}", True, (255, 0, 0))
        text_rect = self.text.get_rect(center=self.rect.center)
        if self.value != 0:
            screen.blit(self.text, text_rect)


class   Game:
    def __init__(self):
        self.running = True
        self.tiles = [[Tile(x, y) for y in range(4)] for x in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].pos = pygame.Vector2(i, j)



def put_random_tile(game):
    random.seed()
    score = (2,) * 9 + (4,)
    empty = [(x, y) for x in range(4) for y in range(4) if game.tiles[x][y].value == 0]
    if not empty:
        return
    x, y = random.choice(empty)
    game.tiles[x][y].value = random.choice(score)


def     start_game(game):
    for i in range(2):
        put_random_tile(game)


if __name__ == '__main__':
    pygame.init()

    font = pygame.font.SysFont("monospace", 46, bold=True)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    game = Game()
    start_game(game)
    while game.running:
        event.handle_events(game ,pygame.event.get())


        for i in range(4):
            for j in range(4):
                game.tiles[i][j].draw(screen)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000

    pygame.quit()