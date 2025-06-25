import pygame
from renderer import GameRenderer


def handle_events(renderer: GameRenderer, events):
    for event in events:
        if event.type == pygame.QUIT:
            renderer.game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                renderer.game.running = False
            if event.key == pygame.K_z or pygame.K_UP == event.key:
                renderer.move(0, -1)
            if event.key == pygame.K_s or pygame.K_DOWN == event.key:
                renderer.move(0, 1)
            if event.key == pygame.K_q or pygame.K_LEFT == event.key:
                renderer.move(-1, 0)
            if event.key == pygame.K_d or pygame.K_RIGHT == event.key:
                renderer.move(1, 0)
            if event.key == pygame.K_r:
                renderer.game.reset()
                renderer.sync_from_logic()
