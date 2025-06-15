import random

import pygame

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
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)  # bordure
        if self.value != 0:
            self.text = font.render(f"{self.value}", True, (255, 0, 255))
            text_rect = self.text.get_rect(center=self.rect.center)
            screen.blit(self.text, text_rect)


class   Game:
    def __init__(self):
        self.running = True
        self.tiles = [[Tile(x, y) for y in range(4)] for x in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].pos = pygame.Vector2(i, j)


def     temp_grid(width, height):
    for i in range(int(SCREEN_HEIGHT / height)):
        pygame.draw.line(screen, (255, 0, 0), (width * i, 0), (width * i, SCREEN_HEIGHT), 1)
    for i in range(int(SCREEN_WIDTH / width)):
        pygame.draw.line(screen, (255, 0, 0), (0, height * i), (SCREEN_WIDTH, height * i), 1)

def     start_game():
    random.seed()
    r1 = random.randrange(4)
    r2 = random.randrange(4)
    game.tiles[random.randrange(4)][random.randrange(4)].value = random.randrange(2, 5, 2)
    game.tiles[random.randrange(4)][random.randrange(4)].value = random.randrange(2, 5, 2)


def     handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False


if __name__ == '__main__':
    pygame.init()

    font = pygame.font.SysFont("monospace", 46)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    game = Game()
    start_game()
    while game.running:
        handle_events(pygame.event.get())


        for i in range(4):
            for j in range(4):
                game.tiles[i][j].draw(screen)

        temp_grid(TILE_SIZE, TILE_SIZE)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000

    pygame.quit()