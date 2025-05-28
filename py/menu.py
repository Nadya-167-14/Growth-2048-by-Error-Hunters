import pygame
import sys

# Gambar dan pygame init akan dipanggil dari main.py
title_image = pygame.image.load("assets/title.png")
background = pygame.image.load("assets/Main menu.png")

start_image_raw = pygame.image.load("assets/start.png")
start_hover_raw = pygame.image.load("assets/start_hover.png")
options_image_raw = pygame.image.load("assets/options.png")
options_hover_raw = pygame.image.load("assets/options_hover.png")
detail_image_raw = pygame.image.load("assets/detail.png")
detail_hover_raw = pygame.image.load("assets/detail_hover.png")

class Button:
    def __init__(self, pos, size, image, hover_image, action_name):
        self.original_image = image
        self.original_hover_image = hover_image
        self.resize(pos, size)
        self.hovered = False
        self.action_name = action_name

    def resize(self, pos, size):
        self.image = pygame.transform.scale(self.original_image, size)
        self.hover_image = pygame.transform.scale(self.original_hover_image, size)
        self.rect = self.image.get_rect(center=pos)

    def draw(self, surface):
        surface.blit(self.hover_image if self.hovered else self.image, self.rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return self.hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def get_scaled_buttons(screen_width, screen_height):
    button_width = int(screen_width * 0.45)
    button_height = int(screen_height * 0.16)
    center_x = screen_width // 2
    start_y = int(screen_height * 0.4)
    spacing = int(button_height * 1.3)

    return [
        Button((center_x, start_y), (button_width, button_height), start_image_raw, start_hover_raw, "PLAY"),
        Button((center_x, start_y + spacing), (button_width, button_height), options_image_raw, options_hover_raw, "OPTIONS"),
        Button((center_x, start_y + 2 * spacing), (button_width, button_height), detail_image_raw, detail_hover_raw, "DETAIL"),
    ]

def draw_scaled_elements(screen, screen_width, screen_height):
    # Background
    bg_scaled = pygame.transform.scale(background, (screen_width, screen_height))
    screen.blit(bg_scaled, (0, 0))

    # Title
    title_width = int(screen_width * 0.5)
    title_height = int(screen_height * 0.18)
    title_scaled = pygame.transform.scale(title_image, (title_width, title_height))
    screen.blit(title_scaled, (screen_width // 2 - title_width // 2, int(screen_height * 0.08)))

def show_menu(screen):
    pygame.mixer.music.load("assets/sfx/backsound.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    clock = pygame.time.Clock()
    screen_width, screen_height = screen.get_size()
    buttons = get_scaled_buttons(screen_width, screen_height)

    while True:
        screen_width, screen_height = screen.get_size()
        draw_scaled_elements(screen, screen_width, screen_height)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                buttons = get_scaled_buttons(event.w, event.h)

            for button in buttons:
                if button.is_clicked(event):
                    if button.action_name == "PLAY":
                        if button.action_name == "PLAY":
                            pygame.mixer.music.fadeout(1000)  
                        return  

        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
