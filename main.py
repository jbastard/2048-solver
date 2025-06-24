import random
import pygame

TILE_SIZE       = 200
SCREEN_WIDTH    = 800
SCREEN_HEIGHT   = 800
FPS             = 60

BACKGROUND_COLOR = (255, 222, 173)

DIRECTION_VECTORS = {
    'up': (0, 1),
    'down': (0, -1),
    'left': (1, 0),
    'right': (-1, 0),
}

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
    for _ in range(2):
        put_random_tile(game)

def     get_line(game, x, y, dx, dy):
    return [game.tiles[x + i * dx][y + i * dy] for i in range(4)]

def     set_line(game, x, y, dx, dy, values):
    for i, val in enumerate(values):
        game.tiles[x + i * dx][y + i * dy].value = val

def     compress_and_merge(values):
    new = [v for v in values if v != 0]
    merged = []
    skip = False
    for i in range(len(new)):
        if skip:
            skip = False
            continue
        if i + 1 < len(new) and new[i] == new[i + 1]:
            merged.append(new[i] * 2)
            skip = True
        else:
            merged.append(new[i])
    merged += [0] * (4 - len(merged))
    return merged

def     move(game, direction):
    if direction not in DIRECTION_VECTORS:
        return

    dx, dy = DIRECTION_VECTORS[direction]
    moved = False

    for i in range(4):
        if dx == 0:
            x, y = i, 0 if dy == 1 else 3
        else:
            x, y = 0 if dx == 1 else 3, i
        line = get_line(game, x, y, dx, dy)
        values = [tile.value for tile in line]
        merged = compress_and_merge(values)
        if values != line:
            moved = True
        set_line(game, x, y, dx, dy, merged)

    if moved:
        put_random_tile(game)

def     handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
            elif event.key in (pygame.K_UP, pygame.K_z):
                move(game, 'up')
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                move(game, 'down')
            elif event.key in (pygame.K_LEFT, pygame.K_q):
                move(game, 'left')
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                move(game, 'right')

if __name__ == '__main__':
    pygame.init()

    font = pygame.font.SysFont("monospace", 46)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0

    game = Game()
    start_game(game)
    while game.running:
        handle_events(pygame.event.get())

        screen.fill(BACKGROUND_COLOR)
        for i in range(4):
            for j in range(4):
                game.tiles[i][j].draw(screen)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000

    pygame.quit()