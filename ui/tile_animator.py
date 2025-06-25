# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tile_animator.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cpoulain <cpoulain@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/25 16:51:49 by cpoulain          #+#    #+#              #
#    Updated: 2025/06/25 17:46:56 by cpoulain         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pygame
from core.tile import Tile

class	TileAnimator:
    def __init__(self):
        self.animations = []

    def animate_spawn(self, tile: Tile):
        tile.scale = 0.0
        tile.animating = True
        tile.animation_type = "spawn"
        tile.animation_start = pygame.time.get_ticks()
        if tile not in self.animations:
            self.animations.append(tile)

    def animate_move(self, tile: Tile, from_pos, to_pos):
        tile.screen_pos = pygame.Vector2(from_pos)
        tile.target_screen_pos = pygame.Vector2(to_pos)
        tile.animating = True
        tile.animation_type = "move"
        tile.animation_start = pygame.time.get_ticks()
        tile.pending_merge = False
        if tile not in self.animations:
            self.animations.append(tile)

    def animate_merge(self, tile: Tile):
        if tile.animating and tile.animation_type == "move":
            tile.pending_merge = True
            return
        tile.animating = True
        tile.animation_type = "merge"
        tile.animation_start = pygame.time.get_ticks()
        tile.pending_merge = False
        if tile not in self.animations:
            self.animations.append(tile)

    def update_animations(self):
        current_time = pygame.time.get_ticks()
        still_animating = []

        for tile in self.animations:
            elapsed = current_time - tile.animation_start
            t = min(elapsed / tile.animation_duration, 1.0)

            match (tile.animation_type):
                case "move":
                    tile.screen_pos = tile.screen_pos.lerp(tile.target_screen_pos, t)
                case "spawn":
                    tile.scale = t if t < 1.0 else 1.0
                case "merge":
                    tile.scale = 1.0 + 0.15 * (1 - (2 * t - 1)**2)

            if t < 1.0:
                still_animating.append(tile)
            else:
                if tile.animation_type == "move" and tile.pending_merge:
                    tile.animation_type = "merge"
                    tile.animation_start = current_time
                    tile.pending_merge = False
                    still_animating.append(tile)
                    continue
                tile.animating = False
                tile.scale = 1.0
                tile.screen_pos = tile.target_screen_pos

        self.animations = still_animating
