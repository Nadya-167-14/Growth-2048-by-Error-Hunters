import pygame
import random
import sys
import os

pygame.init()
pygame.display.set_caption("2048 Growth")

WIDTH, HEIGHT = 500, 600
GRID_SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
FONT = pygame.font.SysFont("Helvetica", 40, bold=True)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


colors = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

tile_images = {}
for value in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
    path = f"assets/{value}.png"
    if os.path.exists(path):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        tile_images[value] = image


GRID_WIDTH = GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * TILE_MARGIN
grid_x_offset = (WIDTH - GRID_WIDTH) // 2

class Game2048:
    def __init__(self):
        self.matrix = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
        self.add_new_tile()
        self.add_new_tile()

    def draw(self):
        screen.fill((250, 246, 227))

        grid_rect = pygame.Rect(
            grid_x_offset,
            100,
            GRID_WIDTH,
            GRID_WIDTH
        )
        pygame.draw.rect(screen, (187, 173, 160), grid_rect, border_radius=12)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.matrix[i][j]
                color = colors.get(value, (160, 137, 99))
                rect = pygame.Rect(
                    grid_x_offset + j * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                    100 + i * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(screen, color, rect, border_radius=12)

                if value in tile_images:
                    screen.blit(tile_images[value], rect.topleft)



    def add_new_tile(self):
        empty = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.matrix[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.matrix[i][j] = 4 if random.random() > 0.9 else 2

    def move(self, direction):
        def transpose(mat): return [list(row) for row in zip(*mat)]
        def reverse(mat): return [row[::-1] for row in mat]
        def compress(mat):
            new = []
            for row in mat:
                new_row = [i for i in row if i != 0]
                new_row += [0] * (GRID_SIZE - len(new_row))
                new.append(new_row)
            return new
        def merge(mat):
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE - 1):
                    if mat[i][j] == mat[i][j+1] and mat[i][j] != 0:
                        mat[i][j] *= 2
                        mat[i][j+1] = 0
            return mat

        old = [row[:] for row in self.matrix]
        mat = self.matrix
        if direction == "up":
            mat = transpose(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = transpose(mat)
        elif direction == "down":
            mat = transpose(mat)
            mat = reverse(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = reverse(mat)
            mat = transpose(mat)
        elif direction == "left":
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
        elif direction == "right":
            mat = reverse(mat)
            mat = compress(mat)
            mat = merge(mat)
            mat = compress(mat)
            mat = reverse(mat)

        if mat != old:
            self.matrix = mat
            self.add_new_tile()

def main():
    game = Game2048()
    running = True

    while running:
        screen.fill((250, 248, 239))
        game.draw()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
