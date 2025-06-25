# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    board_manager.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cpoulain <cpoulain@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/25 17:20:02 by cpoulain          #+#    #+#              #
#    Updated: 2025/06/25 17:52:25 by cpoulain         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
from typing import List
from core.tile import Tile
from ui.tile_animator import TileAnimator
from utils.vector import DIRECTION_VECTORS

class BoardManager:
    def __init__(self, tiles: List[List[Tile]], animator: TileAnimator = None):
        self.tiles = tiles
        self.animator = animator
        self.size = len(tiles)

    def put_random_tile(self):
        values = (2,) * 9 + (4,)
        empty = [(x, y) for x in range(self.size) for y in range(self.size)
                 if self.tiles[x][y].value == 0]
        if empty:
            x, y = random.choice(empty)
            tile = self.tiles[x][y]
            tile.value = random.choice(values)
            if self.animator:
                self.animator.animate_spawn(tile)

    def get_line(self, x, y, dx, dy):
        return [self.tiles[x + i * dx][y + i * dy] for i in range(self.size)]

    def set_line(self, x, y, dx, dy, new_values):
        for i, val in enumerate(new_values):
            tile = self.tiles[x + i * dx][y + i * dy]
            if val != 0 and tile.value != val:
                if self.animator and tile.value != 0:
                    self.animator.animate_merge(tile)
            tile.value = val

    def compress_and_merge_tiles(self, tiles):
        new = [tile for tile in tiles if tile.value != 0]
        result = []
        score = 0
        skip = False

        i = 0
        while i < len(new):
            if not skip and i + 1 < len(new) and new[i].value == new[i + 1].value:
                # Merge
                merged_tile = new[i]
                merged_tile.value *= 2
                score += merged_tile.value
                result.append(merged_tile)
                skip = True
            else:
                if skip:
                    skip = False
                else:
                    result.append(new[i])
            i += 1

        # Pad with dummy tiles (zero-valued) to maintain length
        while len(result) < self.size:
            result.append(Tile(-1, -1))  # dummy placeholder

        return result, score

    def move(self, direction, game):
        if direction not in DIRECTION_VECTORS:
            return

        dx, dy = DIRECTION_VECTORS[direction]
        moved = False
        total_score = 0

        for i in range(self.size):
            # Get line of tiles in the correct direction
            x, y = (i, 0 if dy == 1 else 3) if dx == 0 else (0 if dx == 1 else 3, i)
            line = self.get_line(x, y, dx, dy)
            tiles = [tile for tile in line if tile.value != 0]

            new_line = []
            skip = False
            j = 0

            while j < len(tiles):
                current = tiles[j]
                if not skip and j + 1 < len(tiles) and tiles[j].value == tiles[j + 1].value:
                    # Merge
                    current.value *= 2
                    total_score += current.value
                    if self.animator:
                        self.animator.animate_merge(current)
                    skip = True
                else:
                    skip = False
                new_line.append(current)
                j += 2 if skip else 1

            # Fill with empty tiles to fit the row
            while len(new_line) < self.size:
                new_line.append(None)

            # Animate and apply the result to self.tiles
            for idx, new_tile in enumerate(new_line):
                dest_x = x + idx * dx
                dest_y = y + idx * dy
                dest_tile = self.tiles[dest_x][dest_y]

                old_value = dest_tile.value
                new_value = new_tile.value if new_tile else 0

                if new_tile and new_tile != dest_tile and new_tile.value != 0:
                    if self.animator:
                        self.animator.animate_move(new_tile, new_tile.rect.topleft, dest_tile.rect.topleft)

                dest_tile.value = new_value

            if [tile.value for tile in line] != [t.value if t else 0 for t in new_line]:
                moved = True

        if moved:
            self.put_random_tile()
            game.score += total_score
            print(f"Score : {game.score}")

