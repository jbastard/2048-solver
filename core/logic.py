# logic.py

import random
from utils.vector import DIRECTION_VECTORS

def put_random_tile(tiles):
    values = (2,) * 9 + (4,)
    empty = [(x, y) for x in range(4) for y in range(4) if tiles[x][y].value == 0]
    if empty:
        x, y = random.choice(empty)
        tiles[x][y].value = random.choice(values)

def get_line(tiles, x, y, dx, dy):
    return [tiles[x + i * dx][y + i * dy] for i in range(4)]

def set_line(tiles, x, y, dx, dy, values):
    for i, val in enumerate(values):
        tiles[x + i * dx][y + i * dy].value = val

def compress_and_merge(values):
    new = [v for v in values if v != 0]
    merged, skip = [], False
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

def move(tiles, direction):
    if direction not in DIRECTION_VECTORS:
        return
    dx, dy = DIRECTION_VECTORS[direction]
    moved = False
    for i in range(4):
        x, y = (i, 0 if dy == 1 else 3) if dx == 0 else (0 if dx == 1 else 3, i)
        line = get_line(tiles, x, y, dx, dy)
        values = [tile.value for tile in line]
        merged = compress_and_merge(values)
        if values != merged:
            moved = True
        set_line(tiles, x, y, dx, dy, merged)
    if moved:
        put_random_tile(tiles)
