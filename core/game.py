# game.py

import random
from core.logic import move, put_random_tile
from core.tile import Tile

class Game:
    def __init__(self):
        self.running = True
        self.tiles = [[Tile(x, y) for y in range(4)] for x in range(4)]

    def start(self):
        for _ in range(2):
            put_random_tile(self.tiles)

    def handle_event(self, event):
        from pygame import QUIT, KEYDOWN, K_ESCAPE, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_s, K_q, K_d

        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                self.running = False
            elif event.key in (K_UP, K_z):
                move(self.tiles, 'up')
            elif event.key in (K_DOWN, K_s):
                move(self.tiles, 'down')
            elif event.key in (K_LEFT, K_q):
                move(self.tiles, 'left')
            elif event.key in (K_RIGHT, K_d):
                move(self.tiles, 'right')
