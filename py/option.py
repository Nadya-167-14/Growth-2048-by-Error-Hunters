import pygame
import sys
from ui import get_font

pygame.init()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Options")

font = get_font("font_pixel_small")

bg_image = pygame.image.load("assets/bg_option.png")
bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))

sound_on_img = pygame.image.load("assets/VOLUME 1.png")
sound_off_img = pygame.image.load("assets/VOLUME 2.png")
sound_on_img = pygame.transform.scale(sound_on_img, (500, 200))
sound_off_img = pygame.transform.scale(sound_off_img, (500, 200))

button_rect = sound_on_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

pygame.mixer.music.load("assets/sfx/backsound.mp3")
pygame.mixer.music.set_volume(1.0)
pygame.mixer.music.play(-1)

sound_on = True

def draw_options():
    screen.blit(bg_image, (0, 0))
    img = sound_on_img if sound_on else sound_off_img
    screen.blit(img, button_rect)
    instr1 = font.render("Klik ikon untuk mute", True, (50, 50, 50))
    instr2 = font.render("Klik ESC untuk kembali", True, (50, 50, 50))
    screen.blit(instr1, (WIDTH // 2 - instr1.get_width() // 2, 150))
    screen.blit(instr2, (WIDTH // 2 - instr2.get_width() // 2, HEIGHT - 120))
    pygame.display.flip()

def options_menu():
    global sound_on
    running = True
    while running:
        draw_options()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button_rect.collidepoint(event.pos):
                    sound_on = not sound_on
                    if sound_on:
                        pygame.mixer.music.set_volume(1.0)
                    else:
                        pygame.mixer.music.set_volume(0.0)

def is_sound_on():
    return sound_on
