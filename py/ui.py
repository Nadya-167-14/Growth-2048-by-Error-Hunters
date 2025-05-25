import pygame
import os

# Konstanta
grid_size = 4
tile_size = 100
tile_margin = 10
width, height = 500, 600

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

tile_images = {}
for value in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
    path = f"assets/{value}.png"
    if os.path.exists(path):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (tile_size, tile_size))
        tile_images[value] = image

def draw_game(screen, game):
    grid_width = grid_size * tile_size + (grid_size - 1) * tile_margin
    grid_height = grid_width 

    screen_width, screen_height = screen.get_size()

    offset_x = (screen_width - grid_width) // 2
    offset_y = (screen_height - grid_height) // 2

    for row in range(grid_size):
        for col in range(grid_size):
            x = offset_x + col * (tile_size + tile_margin)
            y = offset_y + row * (tile_size + tile_margin)
            pygame.draw.rect(screen, colors[0], (x, y, tile_size, tile_size), border_radius=8)

    for tile in game.tiles:
        if tile.animation and tile.animation.active:
            row, col = tile.animation.get_current_position()
        else:
            row, col = tile.row, tile.col

        x = offset_x + col * (tile_size + tile_margin)
        y = offset_y + row * (tile_size + tile_margin)
        draw_tile(screen, tile.value, x, y)

def draw_tile(screen, value, x, y):
    rect = pygame.Rect(x, y, tile_size, tile_size)

    if value in tile_images:
        screen.blit(tile_images[value], rect)
    else:
        pygame.draw.rect(screen, colors.get(value, (60, 58, 50)), rect, border_radius=8)
        if value > 0:
            font = pygame.font.Font(None, 40)
            text = font.render(str(value), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def draw_game_over(screen):
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rect = text.get_rect(center=screen.get_rect().center)
    screen.blit(text, text_rect)
