import pygame
from core.game import Game
from ui.renderer import Renderer
from ui.assets import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2048")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 46, bold=True)

    game = Game()
    renderer = Renderer(screen, font, game)
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