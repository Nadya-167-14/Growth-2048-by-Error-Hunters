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

class BombAnimation:
    def __init__(self, pos):
        self.frames = [
            pygame.transform.scale(pygame.image.load(f"assets/bomb/anim_bomb{i}.png").convert_alpha(), (150, 150))
            for i in range(1, 7)
        ]
        self.index = 0
        self.pos = (pos[0] - 25, pos[1] - 25)
        self.finished = False
        self.frame_delay = 4
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.frame_delay:
            self.index += 1
            self.counter = 0
            if self.index >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.frames[self.index], self.pos)


class PupukAnimation:
    def __init__(self, pos):
        self.frames = [
            pygame.transform.scale(pygame.image.load(f"assets/pupuk/anim_pupuk{i}.png"), (150, 150))
            for i in range(1, 7)
        ]
        self.pos = (pos[0] - 25, pos[1] - 25)
        self.index = 0
        self.timer = 0
        self.active = True

    def update(self, dt):
        self.timer += dt
        if self.timer > 80:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.active = False

    def draw(self, surface):
        if self.active and self.index < len(self.frames):
            surface.blit(self.frames[self.index], self.pos)
