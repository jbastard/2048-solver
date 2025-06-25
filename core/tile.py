# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    tile.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cpoulain <cpoulain@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/25 17:20:19 by cpoulain          #+#    #+#              #
#    Updated: 2025/06/25 17:20:20 by cpoulain         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pygame
from ui.assets import TILE_SIZE

class Tile:
    def __init__(self, x, y, offset_x=0, offset_y=0):
        self.value = 0
        self.pos = pygame.Vector2(x, y)
        self.rect = pygame.Rect(offset_x + x * TILE_SIZE,
                                offset_y + y * TILE_SIZE,
                                TILE_SIZE,
                                TILE_SIZE)
        self.screen_pos = pygame.Vector2(self.rect.topleft)  # for animation
        self.animating = False
        self.animation_type = None
        self.animation_start = 0
        self.animation_duration = 200  # ms
        self.target_screen_pos = self.screen_pos
        self.scale = 1.0
        self.just_merged = False
