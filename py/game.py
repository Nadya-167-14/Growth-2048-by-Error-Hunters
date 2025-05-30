import random
import pygame
from animation import TileAnimation

class Tile:
    def __init__(self, row, col, value):
        self.row = row
        self.col = col
        self.value = value
        self.animation = None 

    def set_position(self, row, col):
        self.row = row
        self.col = col

    def move_to(self, new_row, new_col):
        self.animation = TileAnimation((self.row, self.col), (new_row, new_col))
        self.set_position(new_row, new_col)

class Game2048:
    def __init__(self, screen_width, screen_height): 
        self.grid_size = 4
        self.tiles = []
        self.score = 0
        self.matrix = [[None]*self.grid_size for _ in range(self.grid_size)]
        self.active_powerup = None
        
        self.TILE_SIZE = 100 
        self.TILE_SPACING = 10 
        self.total_board_dimension = self.grid_size * self.TILE_SIZE + (self.grid_size + 1) * self.TILE_SPACING
        self.BOARD_X_OFFSET = (screen_width - self.total_board_dimension) // 2
        self.BOARD_Y_OFFSET = (screen_height - self.total_board_dimension) // 3.5

        self.move_sfx = pygame.mixer.Sound("assets/sfx/move.wav")
        self.merge_sfx = pygame.mixer.Sound("assets/sfx/merge.wav")
        self.move_sfx.set_volume(0.5)
        self.merge_sfx.set_volume(0.6)

        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty = [(i, j) for i in range(self.grid_size) for j in range(self.grid_size) if self.matrix[i][j] is None]
        if empty:
            i, j = random.choice(empty)
            value = 4 if random.random() > 0.9 else 2
            tile = Tile(i, j, value)
            self.matrix[i][j] = tile
            self.tiles.append(tile)

    def move(self, direction):
        def transpose(mat):
            return [list(row) for row in zip(*mat)]

        def reverse(mat):
            return [row[::-1] for row in mat]

        def compress(mat):
            new_mat = []
            for row in mat:
                new_row = [tile for tile in row if tile is not None]
                new_row += [None] * (self.grid_size - len(new_row))
                new_mat.append(new_row)
            return new_mat

        def merge(mat):
            score_gained = 0
            merged_any = False
            for i in range(self.grid_size):
                for j in range(self.grid_size - 1):
                    a, b = mat[i][j], mat[i][j + 1]
                    if a and b and a.value == b.value:
                        a.value *= 2
                        if not a.animation:
                            a.animation = TileAnimation((i, j), (i, j))
                            a.animation.start_bounce()
                        score_gained += a.value
                        mat[i][j + 1] = None
                        self.tiles.remove(b)
                        merged_any = True
            if merged_any:
                self.merge_sfx.play()
            return mat, score_gained

        old = [[tile.value if tile else 0 for tile in row] for row in self.matrix]
        mat = self.matrix
        score_this_move = 0

        if direction == "up":
            mat = transpose(mat)
            mat = compress(mat)
            mat, gained = merge(mat)
            score_this_move += gained
            mat = compress(mat)
            mat = transpose(mat)
        elif direction == "down":
            mat = transpose(mat)
            mat = reverse(mat)
            mat = compress(mat)
            mat, gained = merge(mat)
            score_this_move += gained
            mat = compress(mat)
            mat = reverse(mat)
            mat = transpose(mat)
        elif direction == "left":
            mat = compress(mat)
            mat, gained = merge(mat)
            score_this_move += gained
            mat = compress(mat)
        elif direction == "right":
            mat = reverse(mat)
            mat = compress(mat)
            mat, gained = merge(mat)
            score_this_move += gained
            mat = compress(mat)
            mat = reverse(mat)

        moved_any = False
        new_positions = {}
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile = mat[i][j]
                if tile:
                    new_positions[tile] = (i, j)

        for tile, (new_row, new_col) in new_positions.items():
            if (tile.row, tile.col) != (new_row, new_col):
                tile.move_to(new_row, new_col)
                moved_any = True

        self.matrix = mat
        self.score += score_this_move

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile = self.matrix[i][j]
                if tile:
                    tile.set_position(i, j)

        new_state = [[tile.value if tile else 0 for tile in row] for row in self.matrix]
        if old != new_state:
            if moved_any:
                self.move_sfx.play()
            self.add_new_tile()

    def is_game_over(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                tile = self.matrix[i][j]
                if tile is None:
                    return False
                if j + 1 < self.grid_size and self.matrix[i][j + 1] is not None:
                    if tile.value == self.matrix[i][j + 1].value:
                        return False
                if i + 1 < self.grid_size and self.matrix[i + 1][j] is not None:
                    if tile.value == self.matrix[i + 1][j].value:
                        return False
        return True

    def has_won(self):
        for row in self.matrix:
            for tile in row:
                if tile and tile.value == 2048:
                    return True
        return False

    def get_tile_draw_pos(self, row, col):
        x_pos = self.BOARD_X_OFFSET + col * (self.TILE_SIZE + self.TILE_SPACING) + self.TILE_SPACING
        y_pos = self.BOARD_Y_OFFSET + row * (self.TILE_SIZE + self.TILE_SPACING) + self.TILE_SPACING
        return x_pos, y_pos

    def get_board_coords(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        board_end_x = self.BOARD_X_OFFSET + self.grid_size * (self.TILE_SIZE + self.TILE_SPACING) + self.TILE_SPACING
        board_end_y = self.BOARD_Y_OFFSET + self.grid_size * (self.TILE_SIZE + self.TILE_SPACING) + self.TILE_SPACING
        if not (self.BOARD_X_OFFSET <= mouse_x < board_end_x and
                self.BOARD_Y_OFFSET <= mouse_y < board_end_y):
            return None, None

        relative_x = mouse_x - self.BOARD_X_OFFSET
        relative_y = mouse_y - self.BOARD_Y_OFFSET

        col = (relative_x - self.TILE_SPACING) // (self.TILE_SIZE + self.TILE_SPACING)
        row = (relative_y - self.TILE_SPACING) // (self.TILE_SIZE + self.TILE_SPACING)

        if 0 <= row < self.grid_size and 0 <= col < self.grid_size:
            tile_start_x = self.TILE_SPACING + col * (self.TILE_SIZE + self.TILE_SPACING)
            tile_start_y = self.TILE_SPACING + row * (self.TILE_SIZE + self.TILE_SPACING)
            if (relative_x >= tile_start_x and relative_x < tile_start_x + self.TILE_SIZE and
                relative_y >= tile_start_y and relative_y < tile_start_y + self.TILE_SIZE):
                return row, col
        return None, None
