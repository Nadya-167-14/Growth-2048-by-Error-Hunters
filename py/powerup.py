import pygame
pygame.mixer.init()

# Load sound effects
powerup_sounds = {
    "pupuk": pygame.mixer.Sound("assets/sfx/pupuk.wav"),
    "penyiram_otomatis": pygame.mixer.Sound("assets/sfx/siram.wav"),
    "bom": pygame.mixer.Sound("assets/sfx/bom.wav")
}

def play_powerup_sfx(powerup_name):
    sound = powerup_sounds.get(powerup_name)
    if sound:
        sound.play()


def pupuk(game_instance, row, col):
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        if game_instance.matrix[row][col] is not None:
            game_instance.matrix[row][col].value *= 2
            game_instance.score += game_instance.matrix[row][col].value
            play_powerup_sfx("pupuk")
        else:
            return
    else:
        return


def penyiram_otomatis(game_instance):
    game_instance.add_new_tile()
    game_instance.score += 10
    play_powerup_sfx("siram")


def bom(game_instance, row, col):
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        if game_instance.matrix[row][col] is not None:
            removed_tile = game_instance.matrix[row][col]
            removed_value = removed_tile.value

            game_instance.matrix[row][col] = None

            if removed_tile in game_instance.tiles:
                game_instance.tiles.remove(removed_tile)

            game_instance.score -= removed_value // 2
            play_powerup_sfx("bom")
        else:
            return
    else:
        return
