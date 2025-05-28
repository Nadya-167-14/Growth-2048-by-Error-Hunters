import pygame
import os

GLOBAL_TILE_SIZE = 100 
GLOBAL_TILE_MARGIN = 10 

TILE_COLORS = {
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

_ui_assets = {
    "tile_images": {},
    "font_tile": None,
    "font_game_over": None,
    "font_button": None,
}

def init_ui_assets():
    for value in [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048]:
        path = f"assets/{value}.png"
        if os.path.exists(path):
            image = pygame.image.load(path)
            image = pygame.transform.scale(image, (GLOBAL_TILE_SIZE, GLOBAL_TILE_SIZE))
            _ui_assets["tile_images"][value] = image
    
    _ui_assets["font_tile"] = pygame.font.SysFont(None, 48, bold=True)
    _ui_assets["font_game_over"] = pygame.font.SysFont(None, 60, bold=True)
    _ui_assets["font_button"] = pygame.font.SysFont(None, 32)
    _ui_assets["font_pixel_small"] = pygame.font.Font("assets/fonts/pressstart2p.ttf", 16)


go_image = pygame.image.load("assets/go.png")
go_image = pygame.transform.scale(go_image, (300, 150)) 

def get_tile_color(value):
    return TILE_COLORS.get(value, (60, 58, 50))

def draw_tile(screen, value, x, y, tile_dimension):
    rect = pygame.Rect(x, y, tile_dimension, tile_dimension)

    if value in _ui_assets["tile_images"]:
        if tile_dimension != GLOBAL_TILE_SIZE:
            scaled_image = pygame.transform.scale(_ui_assets["tile_images"][value], (tile_dimension, tile_dimension))
            screen.blit(scaled_image, rect)
        else:
            screen.blit(_ui_assets["tile_images"][value], rect)
    else:
        pygame.draw.rect(screen, get_tile_color(value), rect, border_radius=8)
        if value > 0:
            text = _ui_assets["font_tile"].render(str(value), True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

def draw_game(screen, game_instance):
    screen_width, screen_height = screen.get_size()
    
    grid_size = game_instance.grid_size
    tile_dimension = game_instance.TILE_SIZE
    tile_spacing = game_instance.TILE_SPACING
    offset_x = game_instance.BOARD_X_OFFSET 
    offset_y = game_instance.BOARD_Y_OFFSET 

    board_width = grid_size * tile_dimension + (grid_size + 1) * tile_spacing
    board_height = board_width 
    board_rect = pygame.Rect(offset_x, offset_y, board_width, board_height)
    pygame.draw.rect(screen, (187, 173, 160), board_rect, border_radius=5)

    for row in range(grid_size):
        for col in range(grid_size):
            x_pos, y_pos = game_instance.get_tile_draw_pos(row, col)
            pygame.draw.rect(screen, TILE_COLORS[0], (x_pos, y_pos, tile_dimension, tile_dimension), border_radius=8)

    for tile in game_instance.tiles:
        if tile.animation and tile.animation.active:
            anim_row, anim_col = tile.animation.get_current_position()
            x_pos, y_pos = game_instance.get_tile_draw_pos(anim_row, anim_col)
        else:
            x_pos, y_pos = game_instance.get_tile_draw_pos(tile.row, tile.col)
        
        draw_tile(screen, tile.value, x_pos, y_pos, tile_dimension)

    button_width = 150
    button_height = 40
    spacing = 20
    total_buttons_width = button_width * 3 + spacing * 2
    start_x = (screen_width - total_buttons_width) // 2
    y_buttons = 520 

    button_colors = [(200, 100, 100), (100, 200, 100), (100, 100, 200)]
    button_labels = ["Pupuk", "Penyiram", "Bom"]
    powerup_buttons = []

    for i in range(3):
        rect = pygame.Rect(start_x + i * (button_width + spacing), y_buttons, button_width, button_height)
        pygame.draw.rect(screen, button_colors[i], rect, border_radius=8)
        text = _ui_assets["font_button"].render(button_labels[i], True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        powerup_buttons.append(rect)

    if game_instance.active_powerup is not None:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        row, col = game_instance.get_board_coords((mouse_x, mouse_y))
        
        if row is not None and col is not None:
            x_highlight, y_highlight = game_instance.get_tile_draw_pos(row, col)
            
            highlight_color = (255, 255, 0, 150) 
            if game_instance.active_powerup == 'bom':
                highlight_color = (255, 0, 0, 150) 

            s = pygame.Surface((tile_dimension, tile_dimension), pygame.SRCALPHA)
            s.fill(highlight_color)
            screen.blit(s, (x_highlight, y_highlight))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    else:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    return powerup_buttons

def draw_game_over(screen):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    screen_width, screen_height = screen.get_size()

    go_rect = go_image.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 80))
    screen.blit(go_image, go_rect)

    font_pixel = _ui_assets["font_pixel_small"]
    message_lines = [
        "you have skill issues, dude~",
        "better luck next time.."
    ]

    for i, line in enumerate(message_lines):
        text_surface = font_pixel.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen.get_width() // 2, go_rect.bottom + 20 + i * 22))
        screen.blit(text_surface, text_rect)

    button_width, button_height = 160, 40
    button_x = screen_width // 2 - button_width // 2
    button_y = 360
    pygame.draw.rect(screen, (100, 100, 255), (button_x, button_y, button_width, button_height), border_radius=10)

    font_button = _ui_assets["font_pixel_small"]
    menu_text = font_button.render("Back to Menu", True, (255, 255, 255))
    menu_text_rect = menu_text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(menu_text, menu_text_rect)

    # Return rect untuk interaksi klik
    return pygame.Rect(button_x, button_y, button_width, button_height)
