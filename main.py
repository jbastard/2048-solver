import pygame
from constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, FPS, LOGO_SIZE, SCORE_SIZE
import tile
import game as game_module
import event_handler as event

if __name__ == '__main__':
    pygame.init()

    tile.game_font = pygame.font.SysFont("monospace", int(TILE_SIZE / 4), bold=True)
    game_module.logo_font = pygame.font.SysFont("monospace", LOGO_SIZE, bold=True)
    game_module.score_font = pygame.font.SysFont("monospace", SCORE_SIZE, bold=True)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    clock = pygame.time.Clock()
    dt = 0

    game = game_module.Game()
    game_module.start_game(game)
    while game.running:
        event.handle_events(game, pygame.event.get())
        game.update(dt)
        game.render(screen)
        if game_module.is_game_over(game):
            game_module.render_game_over(screen)
        pygame.display.flip()
        dt = clock.tick(FPS) / 1000
    pygame.quit()

