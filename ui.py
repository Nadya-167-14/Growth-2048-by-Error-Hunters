import pygame
import os

# Konstanta
GRID_SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
WIDTH, HEIGHT = 500, 600

# Warna tile default
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

# Memuat gambar tile jika tersedia
tile_images = {}
for value in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
    path = f"assets/{value}.png"
    if os.path.exists(path):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        tile_images[value] = image

def draw_game(screen, game):
    # Hitung ukuran total grid
    grid_width = GRID_SIZE * TILE_SIZE + (GRID_SIZE - 1) * TILE_MARGIN
    grid_height = grid_width  # Karena gridnya kotak

    # Ambil ukuran layar saat ini
    screen_width, screen_height = screen.get_size()

    # Hitung posisi offset agar grid berada di tengah
    offset_x = (screen_width - grid_width) // 2
    offset_y = (screen_height - grid_height) // 2

    # Gambar grid kosong
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = offset_x + col * (TILE_SIZE + TILE_MARGIN)
            y = offset_y + row * (TILE_SIZE + TILE_MARGIN)
            pygame.draw.rect(screen, colors[0], (x, y, TILE_SIZE, TILE_SIZE), border_radius=8)

    # Gambar tile dengan nilai
    for tile in game.tiles:
        if tile.animation and tile.animation.active:
            row, col = tile.animation.get_current_position()
        else:
            row, col = tile.row, tile.col

        x = offset_x + col * (TILE_SIZE + TILE_MARGIN)
        y = offset_y + row * (TILE_SIZE + TILE_MARGIN)
        draw_tile(screen, tile.value, x, y)

def draw_tile(screen, value, x, y):
    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    if value in tile_images:
        screen.blit(tile_images[value], rect)
    else:
        pygame.draw.rect(screen, colors.get(value, (60, 58, 50)), rect, border_radius=8)
        if value > 0:
            font = pygame.font.Font(None, 40)
            text = font.render(str(value), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
