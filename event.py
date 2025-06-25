import main
import pygame

def     handle_events(game, events):
    for event in events:
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game.running = False
            if event.key == pygame.K_z or pygame.K_UP == event.key:
                move_tiles(game, 0, -1)
            if event.key == pygame.K_s or pygame.K_DOWN == event.key:
                move_tiles(game, 0, 1)
            if event.key == pygame.K_q or pygame.K_LEFT == event.key:
                move_tiles(game, -1, 0)
            if event.key == pygame.K_d or pygame.K_RIGHT== event.key:
                move_tiles(game, 1, 0)
            if event.key == pygame.K_r:
                main.start_game(game)


def     move_tiles(game, dx, dy):
    moved = False
    merged = [[False for _ in range(4)] for _ in range(4)]

    range_x = range(4) if dx == -1 else range(3, -1, -1) if dx == 1 else range(4)
    range_y = range(4) if dy == -1 else range(3, -1, -1) if dy == 1 else range(4)

    for x in range_x:
        for y in range_y:
            if game.tiles[x][y].value != 0:
                curr_x, curr_y = x, y
                next_x, next_y = x + dx, y + dy
                while 0 <= next_x < 4 and 0 <= next_y < 4 and game.tiles[next_x][next_y].value == 0:
                    game.tiles[next_x][next_y].value = game.tiles[curr_x][curr_y].value
                    game.tiles[curr_x][curr_y].value = 0
                    curr_x, curr_y = next_x, next_y
                    next_x, next_y = curr_x + dx, curr_y + dy
                    moved = True
                if 0 <= next_x < 4 and 0 <= next_y < 4 and game.tiles[next_x][next_y].value == game.tiles[curr_x][curr_y].value and not merged[next_x][next_y]:
                    game.tiles[next_x][next_y].value *= 2
                    game.score += game.tiles[next_x][next_y].value
                    game.tiles[curr_x][curr_y].value = 0
                    merged[next_x][next_y] = True
                    moved = True
    if moved:
        main.put_random_tile(game)
