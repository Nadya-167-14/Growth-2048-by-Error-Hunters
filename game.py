import random

# Dummy class untuk menghindari error jika TileAnimation belum dibuat
class TileAnimation:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.active = False

import animation  # Jika kamu punya modul animasi sendiri, pastikan TileAnimation ada di sana

GRID_SIZE = 4

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
    def __init__(self):
        self.tiles = []
        self.score = 0
        self.matrix = [[None]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.matrix[i][j] is None]
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
                new_row += [None] * (GRID_SIZE - len(new_row))
                new_mat.append(new_row)
            return new_mat

        def merge(mat):
            score_gained = 0
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE - 1):
                    a, b = mat[i][j], mat[i][j + 1]
                    if a and b and a.value == b.value:
                        a.value *= 2
                        score_gained += a.value
                        mat[i][j + 1] = None
                        self.tiles.remove(b)
            return mat, score_gained

        # Simpan kondisi awal
        old = [[tile.value if tile else 0 for tile in row] for row in self.matrix]
        mat = self.matrix
        score_this_move = 0

        # Gerakkan sesuai arah
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

        # Simpan posisi baru setiap tile
        new_positions = {}
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = mat[i][j]
                if tile:
                    new_positions[tile] = (i, j)

        # Update animasi & posisi internal tile
        for tile, (new_row, new_col) in new_positions.items():
            if (tile.row, tile.col) != (new_row, new_col):
                tile.move_to(new_row, new_col)

        self.matrix = mat
        self.score += score_this_move

        # Sinkronisasi posisi tile (untuk memastikan posisi row/col sesuai dengan matrix)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = self.matrix[i][j]
                if tile:
                    tile.set_position(i, j)

        # Tambahkan tile baru jika terjadi perubahan
        new_state = [[tile.value if tile else 0 for tile in row] for row in self.matrix]
        if old != new_state:
            self.add_new_tile()
