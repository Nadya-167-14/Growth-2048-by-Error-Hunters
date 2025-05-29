import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 450, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Options")

WHITE = (255, 255, 255)
font = pygame.font.SysFont("Arial", 20)

sound_on_img = pygame.image.load("assets/VOLUME 1.png")
sound_off_img = pygame.image.load("assets/VOLUME 2.png")

sound_on_img = pygame.transform.scale(sound_on_img, (150, 150))
sound_off_img = pygame.transform.scale(sound_off_img, (150, 150))

button_rect = sound_on_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

sound_on = True

def draw_options():
    screen.fill(WHITE)

    img = sound_on_img if sound_on else sound_off_img
    screen.blit(img, button_rect)

    instr1 = font.render("Click icon to toggle sound", True, (50, 50, 50))
    instr2 = font.render("Press ESC to return", True, (100, 100, 100))

    screen.blit(instr1, (WIDTH // 2 - instr1.get_width() // 2, 50))
    screen.blit(instr2, (WIDTH // 2 - instr2.get_width() // 2, HEIGHT - 60))

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

def is_sound_on():
    return sound_on

