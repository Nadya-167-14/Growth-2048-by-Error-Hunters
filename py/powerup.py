import pygame
from animation import BombAnimation, PupukAnimation

pygame.mixer.init()
active_animations = []

powerup_sounds = {
    "pupuk": pygame.mixer.Sound("assets/sfx/pupuk.mp3"),
    "penyiram_otomatis": pygame.mixer.Sound("assets/sfx/siram.mp3"),
    "bom": pygame.mixer.Sound("assets/sfx/bom.mp3")
}

def play_powerup_sfx(powerup_name):
    sound = powerup_sounds.get(powerup_name)
    if sound:
        sound.play()

def pupuk(game_instance, row, col):
    row = int(row)
    col = int(col)
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        if game_instance.matrix[row][col] is not None:
            game_instance.matrix[row][col].value *= 2
            game_instance.score += game_instance.matrix[row][col].value
            play_powerup_sfx("pupuk")
            x = game_instance.BOARD_X_OFFSET + col * (game_instance.TILE_SIZE + game_instance.TILE_SPACING) + game_instance.TILE_SPACING
            y = game_instance.BOARD_Y_OFFSET + row * (game_instance.TILE_SIZE + game_instance.TILE_SPACING) + game_instance.TILE_SPACING
            active_animations.append(PupukAnimation((x, y)))

def penyiram_otomatis(game):
    game.add_new_tile()
    game.score += 10
    play_powerup_sfx("penyiram_otomatis")

def bom(game_instance, row, col):
    row = int(row)
    col = int(col)
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        if game_instance.matrix[row][col] is not None:
            removed_tile = game_instance.matrix[row][col]
            removed_value = removed_tile.value
            x = game_instance.BOARD_X_OFFSET + col * (game_instance.TILE_SIZE + game_instance.TILE_SPACING) + game_instance.TILE_SPACING
            y = game_instance.BOARD_Y_OFFSET + row * (game_instance.TILE_SIZE + game_instance.TILE_SPACING) + game_instance.TILE_SPACING
            active_animations.append(BombAnimation((x, y)))
            game_instance.matrix[row][col] = None
            if removed_tile in game_instance.tiles:
                game_instance.tiles.remove(removed_tile)
            game_instance.score -= removed_value // 2
            play_powerup_sfx("bom")
