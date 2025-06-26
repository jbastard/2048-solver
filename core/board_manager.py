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

    def moves_available(self) -> bool:
        """Return True if at least one move is possible."""
        # Empty space available
        for x in range(self.size):
            for y in range(self.size):
                if self.tiles[x][y].value == 0:
                    return True

        # Check for possible merges horizontally and vertically
        for x in range(self.size):
            for y in range(self.size):
                val = self.tiles[x][y].value
                if x + 1 < self.size and self.tiles[x + 1][y].value == val:
                    return True
                if y + 1 < self.size and self.tiles[x][y + 1].value == val:
                    return True

        return False

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
        """Move tiles in the given direction and trigger animations."""
        if direction not in DIRECTION_VECTORS:
            return False

        dx, dy = DIRECTION_VECTORS[direction]
        moved = False
        total_score = 0

        def move_tile(src_x, src_y, dst_x, dst_y):
            """Helper that moves the value from src to dst and animates the dst tile."""
            nonlocal moved
            src_tile = self.tiles[src_x][src_y]
            dst_tile = self.tiles[dst_x][dst_y]

            if src_tile == dst_tile:
                return

            if self.animator:
                self.animator.animate_move(dst_tile, src_tile.rect.topleft, dst_tile.rect.topleft)

            dst_tile.value = src_tile.value
            src_tile.value = 0
            moved = True

        if direction == 'up':
            for x in range(self.size):
                last_merge_y = -1
                for y in range(1, self.size):
                    if self.tiles[x][y].value == 0:
                        continue
                    ny = y
                    while ny > 0 and self.tiles[x][ny - 1].value == 0:
                        ny -= 1
                    if ny > 0 and self.tiles[x][ny - 1].value == self.tiles[x][y].value and last_merge_y != ny - 1:
                        move_tile(x, y, x, ny - 1)
                        dst = self.tiles[x][ny - 1]
                        dst.value *= 2
                        dst.just_merged = True
                        total_score += dst.value
                        if self.animator:
                            self.animator.animate_merge(dst)
                        last_merge_y = ny - 1
                    else:
                        move_tile(x, y, x, ny)
        elif direction == 'down':
            for x in range(self.size):
                last_merge_y = self.size
                for y in range(self.size - 2, -1, -1):
                    if self.tiles[x][y].value == 0:
                        continue
                    ny = y
                    while ny + 1 < self.size and self.tiles[x][ny + 1].value == 0:
                        ny += 1
                    if ny + 1 < self.size and self.tiles[x][ny + 1].value == self.tiles[x][y].value and last_merge_y != ny + 1:
                        move_tile(x, y, x, ny + 1)
                        dst = self.tiles[x][ny + 1]
                        dst.value *= 2
                        dst.just_merged = True
                        total_score += dst.value
                        if self.animator:
                            self.animator.animate_merge(dst)
                        last_merge_y = ny + 1
                    else:
                        move_tile(x, y, x, ny)
        elif direction == 'left':
            for y in range(self.size):
                last_merge_x = -1
                for x in range(1, self.size):
                    if self.tiles[x][y].value == 0:
                        continue
                    nx = x
                    while nx > 0 and self.tiles[nx - 1][y].value == 0:
                        nx -= 1
                    if nx > 0 and self.tiles[nx - 1][y].value == self.tiles[x][y].value and last_merge_x != nx - 1:
                        move_tile(x, y, nx - 1, y)
                        dst = self.tiles[nx - 1][y]
                        dst.value *= 2
                        dst.just_merged = True
                        total_score += dst.value
                        if self.animator:
                            self.animator.animate_merge(dst)
                        last_merge_x = nx - 1
                    else:
                        move_tile(x, y, nx, y)
        elif direction == 'right':
            for y in range(self.size):
                last_merge_x = self.size
                for x in range(self.size - 2, -1, -1):
                    if self.tiles[x][y].value == 0:
                        continue
                    nx = x
                    while nx + 1 < self.size and self.tiles[nx + 1][y].value == 0:
                        nx += 1
                    if nx + 1 < self.size and self.tiles[nx + 1][y].value == self.tiles[x][y].value and last_merge_x != nx + 1:
                        move_tile(x, y, nx + 1, y)
                        dst = self.tiles[nx + 1][y]
                        dst.value *= 2
                        dst.just_merged = True
                        total_score += dst.value
                        if self.animator:
                            self.animator.animate_merge(dst)
                        last_merge_x = nx + 1
                    else:
                        move_tile(x, y, nx, y)

        # reset merge flags
        for row in self.tiles:
            for tile in row:
                tile.just_merged = False

        if moved:
            self.put_random_tile()
            game.score += total_score
            print(f"Score : {game.score}")
        return moved
