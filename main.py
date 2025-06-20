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
    score = (2, 2, 2, 2, 2, 2, 2, 2, 2, 4)
    r1 = pygame.Vector2(random.randrange(4), random.randrange(4))
    while game.tiles[int(r1.x)][int(r1.y)].value != 0:
        r1 = pygame.Vector2(random.randrange(4), random.randrange(4))
    game.tiles[int(r1.x)][int(r1.y)].value = score[int(random.randrange(10))]


def     start_game(game):
    for i in range(2):
        put_random_tile(game)


def     move_up(game):
    for row in range(4):
        for column in range(4):
            if game.tiles[column][row].value != 0:
                if row - 1 >= 0 and game.tiles[column][row].value != 0:
                    print(f"{column}, {row - 1}")
                    game.tiles[column][row - 1].value =  game.tiles[column][row].value
                    game.tiles[column][row].value = 0



def     handle_events(events):
    for event in events:
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
            if event.key == pygame.K_z or pygame.K_UP == event.key:
                move_up(game)

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


        for i in range(4):
            for j in range(4):
                game.tiles[i][j].draw(screen)

        pygame.display.flip()
        dt = clock.tick(FPS) / 1000

    pygame.quit()