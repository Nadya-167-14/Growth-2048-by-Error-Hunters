import pygame

class TileAnimation:
    def __init__(self, start_pos, target_pos, duration=150):
        self.start_pos = start_pos
        self.target_pos = target_pos
        self.duration = duration
        self.start_time = pygame.time.get_ticks()
        self.active = True

    def get_current_position(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time

        if elapsed >= self.duration:
            self.active = False
            return self.target_pos

        t = elapsed / self.duration
        x = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * t
        y = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * t
        return x, y
