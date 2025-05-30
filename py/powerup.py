import pygame
from animation import BombAnimation, PupukAnimation

pygame.mixer.init()
active_animations = []

class PowerUp:
    sound_path = None
    def __init__(self, game_instance):
        self.game = game_instance
        self.sound = pygame.mixer.Sound(self.sound_path) if self.sound_path else None

    def play_sfx(self):
        if self.sound:
            self.sound.play()

    def activate(self, *args, **kwargs):
        raise NotImplementedError("Please implement the activate method.")

class PupukPowerUp(PowerUp):
    sound_path = "assets/sfx/pupuk.mp3"

    def activate(self, row, col):
        row, col = int(row), int(col)
        if 0 <= row < self.game.grid_size and 0 <= col < self.game.grid_size:
            tile = self.game.matrix[row][col]
            if tile:
                tile.value *= 2
                self.game.score += tile.value
                self.play_sfx()
                x = self.game.BOARD_X_OFFSET + col * (self.game.TILE_SIZE + self.game.TILE_SPACING) + self.game.TILE_SPACING
                y = self.game.BOARD_Y_OFFSET + row * (self.game.TILE_SIZE + self.game.TILE_SPACING) + self.game.TILE_SPACING
                active_animations.append(PupukAnimation((x, y)))

class PenyiramOtomatisPowerUp(PowerUp):
    sound_path = "assets/sfx/siram.mp3"

    def activate(self):
        self.game.add_new_tile()
        self.game.score += 10
        self.play_sfx()

class BomPowerUp(PowerUp):
    sound_path = "assets/sfx/bom.mp3"

    def activate(self, row, col):
        row, col = int(row), int(col)
        if 0 <= row < self.game.grid_size and 0 <= col < self.game.grid_size:
            tile = self.game.matrix[row][col]
            if tile:
                removed_value = tile.value
                x = self.game.BOARD_X_OFFSET + col * (self.game.TILE_SIZE + self.game.TILE_SPACING) + self.game.TILE_SPACING
                y = self.game.BOARD_Y_OFFSET + row * (self.game.TILE_SIZE + self.game.TILE_SPACING) + self.game.TILE_SPACING
                active_animations.append(BombAnimation((x, y)))
                self.game.matrix[row][col] = None
                if tile in self.game.tiles:
                    self.game.tiles.remove(tile)
                self.game.score -= removed_value // 2
                self.play_sfx()
