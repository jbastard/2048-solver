import pygame
from constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LOGO_SIZE, SCORE_SIZE
import tile
from game_logic import Game
import renderer
import event_handler as event

if __name__ == '__main__':
    pygame.init()

    tile.game_font = pygame.font.SysFont("monospace", int(TILE_SIZE / 4), bold=True)
    renderer.logo_font = pygame.font.SysFont("monospace", LOGO_SIZE, bold=True)
    renderer.score_font = pygame.font.SysFont("monospace", SCORE_SIZE, bold=True)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    dt = 0

    game = Game()
    game.reset()
    view = renderer.GameRenderer(game)

    while game.running:
        event.handle_events(view, pygame.event.get())
        view.update(dt)
        view.render(screen)
        if game.is_game_over():
            renderer.render_game_over(screen)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
    pygame.quit()
