import game
import pygame
import tile


def     handle_events(game_obj, events):
    for event in events:
        if event.type == pygame.QUIT:
            game_obj.running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_obj.running = False
            if event.key == pygame.K_z or pygame.K_UP == event.key:
                move_tiles(game_obj, 0, -1)
            if event.key == pygame.K_s or pygame.K_DOWN == event.key:
                move_tiles(game_obj, 0, 1)
            if event.key == pygame.K_q or pygame.K_LEFT == event.key:
                move_tiles(game_obj, -1, 0)
            if event.key == pygame.K_d or pygame.K_RIGHT== event.key:
                move_tiles(game_obj, 1, 0)
            if event.key == pygame.K_r:
                game.start_game(game_obj)


def     move_tiles(game_obj, dx, dy):
    moved = False
    merged = [[False for _ in range(4)] for _ in range(4)]

    range_x = range(4) if dx == -1 else range(3, -1, -1) if dx == 1 else range(4)
    range_y = range(4) if dy == -1 else range(3, -1, -1) if dy == 1 else range(4)

    for x in range_x:
        for y in range_y:
            if game_obj.tiles[x][y].value != 0:
                val = game_obj.tiles[x][y].value
                curr_x, curr_y = x, y
                next_x, next_y = x + dx, y + dy
                while 0 <= next_x < 4 and 0 <= next_y < 4 and game_obj.tiles[next_x][next_y].value == 0:
                    game_obj.tiles[next_x][next_y].value = game_obj.tiles[curr_x][curr_y].value
                    game_obj.tiles[curr_x][curr_y].value = 0
                    curr_x, curr_y = next_x, next_y
                    next_x, next_y = curr_x + dx, curr_y + dy
                    moved = True
                merge = False
                if 0 <= next_x < 4 and 0 <= next_y < 4 and game_obj.tiles[next_x][next_y].value == game_obj.tiles[curr_x][curr_y].value and not merged[next_x][next_y]:
                    game_obj.tiles[next_x][next_y].value *= 2
                    game_obj.score += game_obj.tiles[next_x][next_y].value
                    game_obj.tiles[curr_x][curr_y].value = 0
                    merged[next_x][next_y] = True
                    moved = True
                    merge = True
                    dest_x, dest_y = next_x, next_y
                else:
                    dest_x, dest_y = curr_x, curr_y

                if dest_x != x or dest_y != y:
                    anim = tile.Tile(dest_x, dest_y, value=val)
                    anim.start_move((x, y), (dest_x, dest_y), 0.1, merge=merge)
                    game_obj.anim_tiles.append(anim)
                    game_obj.tiles[dest_x][dest_y].visible = False
    if moved:
        game.put_random_tile(game_obj)

