# Game logic module separated from rendering
import random

class Game:
    def __init__(self):
        self.score = 0
        self.running = True
        self.board = [[0 for _ in range(4)] for _ in range(4)]

    def reset(self):
        """Start a new game."""
        self.score = 0
        for x in range(4):
            for y in range(4):
                self.board[x][y] = 0
        for _ in range(2):
            self.put_random_tile()

    def put_random_tile(self):
        """Put a new tile on a random empty cell."""
        empty = [(x, y) for x in range(4) for y in range(4) if self.board[x][y] == 0]
        if not empty:
            return None
        x, y = random.choice(empty)
        self.board[x][y] = random.choice((2,) * 9 + (4,))
        return x, y

    def is_game_over(self):
        for x in range(4):
            for y in range(4):
                val = self.board[x][y]
                if val == 0:
                    return False
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 4 and 0 <= ny < 4:
                        if self.board[nx][ny] == val:
                            return False
        return True

    def move(self, dx: int, dy: int):
        """Move tiles on the board. Returns the operations list and the new tile position."""
        moved = False
        merged = [[False for _ in range(4)] for _ in range(4)]
        operations = []

        range_x = range(4) if dx == -1 else range(3, -1, -1) if dx == 1 else range(4)
        range_y = range(4) if dy == -1 else range(3, -1, -1) if dy == 1 else range(4)

        for x in range_x:
            for y in range_y:
                if self.board[x][y] != 0:
                    val = self.board[x][y]
                    curr_x, curr_y = x, y
                    next_x, next_y = x + dx, y + dy
                    while 0 <= next_x < 4 and 0 <= next_y < 4 and self.board[next_x][next_y] == 0:
                        self.board[next_x][next_y] = self.board[curr_x][curr_y]
                        self.board[curr_x][curr_y] = 0
                        curr_x, curr_y = next_x, next_y
                        next_x, next_y = curr_x + dx, curr_y + dy
                        moved = True
                    merge = False
                    if 0 <= next_x < 4 and 0 <= next_y < 4 and self.board[next_x][next_y] == self.board[curr_x][curr_y] and not merged[next_x][next_y]:
                        self.board[next_x][next_y] *= 2
                        self.score += self.board[next_x][next_y]
                        self.board[curr_x][curr_y] = 0
                        merged[next_x][next_y] = True
                        moved = True
                        merge = True
                        dest_x, dest_y = next_x, next_y
                    else:
                        dest_x, dest_y = curr_x, curr_y
                    if dest_x != x or dest_y != y:
                        operations.append({"from": (x, y), "to": (dest_x, dest_y), "value": val, "merge": merge})
        new_tile = None
        if moved:
            new_tile = self.put_random_tile()
        return operations, new_tile
