# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    game.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: cpoulain <cpoulain@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2025/06/25 17:20:12 by cpoulain          #+#    #+#              #
#    Updated: 2025/06/25 17:20:12 by cpoulain         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import random
import pygame
from core.tile import Tile
from ui.assets import SCREEN_HEIGHT, SCREEN_WIDTH, GAME_HEIGHT, GAME_WIDTH
from ui.tile_animator import TileAnimator
from core.board_manager import BoardManager

class Game:
    def __init__(self):
        self.running = True
        offset_x = (SCREEN_WIDTH - GAME_WIDTH) // 2
        offset_y = (SCREEN_HEIGHT - GAME_HEIGHT) - (SCREEN_WIDTH - GAME_WIDTH) // 4
        self.tiles = [[Tile(x, y, offset_x, offset_y) for y in range(4)] for x in range(4)]
        self.rect = pygame.Rect(offset_x,
                                offset_y,
                                GAME_WIDTH,
                                GAME_HEIGHT)
        self.score = 0
        self.board = BoardManager(self.tiles)
        self.animator = None

    def set_animator(self, animator : TileAnimator = None):
        self.board.animator = animator
        self.animator = animator

    def start(self):
        for _ in range(2):
            self.board.put_random_tile()

    def handle_event(self, event):
        from pygame import QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_s, K_q, K_d

        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
            elif event.key in (K_UP, K_z):
                self.board.move('up', self)
            elif event.key in (K_DOWN, K_s):
                self.board.move('down', self)
            elif event.key in (K_LEFT, K_q):
                self.board.move('left', self)
            elif event.key in (K_RIGHT, K_d):
                self.board.move('right', self)
