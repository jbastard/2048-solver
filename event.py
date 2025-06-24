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
                move_up(game)
            if event.key == pygame.K_s or pygame.K_DOWN == event.key:
                move_down(game)
            if event.key == pygame.K_q or pygame.K_LEFT == event.key:
                move_left(game)
            if event.key == pygame.K_d or pygame.K_RIGHT== event.key:
                move_right(game)


def     move_tiles(game, dx, dy):
    moved = False
    merged = [4][4]
    for i in range(4):
        x, y = (i, 0 if dy == 1 else 3) if dx == 0 else (0 if dx == 1 else 3, i)
        for row in range(x, 4, dx) if dx == 1 else range(x, -1, dx):
            for column in range(y, 4, dy) if dy == 1 else range(y, -1, dy):
                temp_row, temp_column = row, column
                while game.tiles[temp_column][temp_row].value:



def     move_down(game):
    moved = 0
    for row in range(3, -1, -1):
        for column in range(4):
            if game.tiles[column][row].value != 0:
                temp_row = row + 1
                while temp_row < 4 and game.tiles[column][temp_row].value == 0:
                    game.tiles[column][temp_row].value = game.tiles[column][temp_row - 1].value
                    game.tiles[column][temp_row - 1].value = 0
                    temp_row += 1
                    moved = 1
                if temp_row < 4 and game.tiles[column][temp_row - 1].value == game.tiles[column][temp_row].value:
                    game.tiles[column][temp_row].value *= 2
                    game.tiles[column][temp_row - 1].value = 0
                    moved = 1
    if moved:
        main.put_random_tile(game)

def     move_up(game):
    moved = 0
    for row in range(4):
        for column in range(4):
            if game.tiles[column][row].value != 0:
                temp_row = row - 1
                while temp_row >= 0 and game.tiles[column][temp_row].value == 0:
                    game.tiles[column][temp_row].value = game.tiles[column][temp_row + 1].value
                    game.tiles[column][temp_row + 1].value = 0
                    temp_row -= 1
                    moved = 1
                if game.tiles[column][temp_row + 1].value == game.tiles[column][temp_row].value:
                    game.tiles[column][temp_row].value *= 2
                    game.tiles[column][temp_row + 1].value = 0
                    moved = 1
    if moved:
        main.put_random_tile(game)

def     move_left(game):
    moved = 0
    for column in range(4):
        for row in range(4):
            if game.tiles[column][row].value != 0:
                temp_column = column - 1
                while temp_column >= 0 and game.tiles[temp_column][row].value == 0:
                    game.tiles[temp_column][row].value = game.tiles[temp_column + 1][row].value
                    game.tiles[temp_column + 1][row].value = 0
                    temp_column -= 1
                    moved = 1
                if game.tiles[temp_column + 1][row].value == game.tiles[temp_column][row].value:
                    game.tiles[temp_column][row].value *= 2
                    game.tiles[temp_column + 1][row].value = 0
                    moved = 1
    if moved:
        main.put_random_tile(game)

def move_right(game):
    moved = 0
    for column in range(3, -1, -1):
        for row in range(4):
            if game.tiles[column][row].value != 0:
                temp_column = column + 1
                while temp_column < 4 and game.tiles[temp_column][row].value == 0:
                    game.tiles[temp_column][row].value = game.tiles[temp_column - 1][row].value
                    game.tiles[temp_column - 1][row].value = 0
                    temp_column += 1
                    moved = 1
                if temp_column < 4 and game.tiles[temp_column - 1][row].value == game.tiles[temp_column][row].value:
                    game.tiles[temp_column][row].value *= 2
                    game.tiles[temp_column - 1][row].value = 0
                    moved = 1
    if moved:
        main.put_random_tile(game)
