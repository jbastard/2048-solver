import pygame
from core.game import Game
from ui.renderer import Renderer
from ui.tile_animator import TileAnimator
from ui.assets import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TILE_SIZE

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", TILE_SIZE // 4, bold=True)

    animator = TileAnimator()
    game = Game(animator=animator)
    renderer = Renderer(screen, font, game, animator)
    game.start()

    while game.running:
        for event in pygame.event.get():
            game.handle_event(event)

        renderer.draw_board(game.tiles, game.score)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
