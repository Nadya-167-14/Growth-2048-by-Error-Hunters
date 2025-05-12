import pygame
import sys
import subprocess
import os

pygame.init()
screen = pygame.display.set_mode((450, 450))
clock = pygame.time.Clock()

# Gambar
title_image = pygame.image.load("assets/title.png")
title_image = pygame.transform.scale(title_image, (200, 80)) 
background = pygame.image.load("assets/Main menu.png")

start_image = pygame.image.load("assets/start.png")
start_hover = pygame.image.load("assets/start_hover.png")
options_image = pygame.image.load("assets/options.png")  
options_hover = pygame.image.load("assets/options_hover.png")
detail_image = pygame.image.load("assets/detail.png")  
detail_hover = pygame.image.load("assets/detail_hover.png")

# Skala gambar tombol
start_image = pygame.transform.scale(start_image, (200, 50))
start_hover = pygame.transform.scale(start_hover, (200, 50))
options_image = pygame.transform.scale(options_image, (200, 50))
options_hover = pygame.transform.scale(options_hover, (200, 50))
detail_image = pygame.transform.scale(detail_image, (200, 50))
detail_hover = pygame.transform.scale(detail_hover, (200, 50))

class Button:
    def __init__(self, pos, image, hover_image, action_name):
        self.image = image
        self.hover_image = hover_image
        self.rect = self.image.get_rect(center=pos)
        self.hovered = False
        self.action_name = action_name

    def draw(self, surface):
        surface.blit(self.hover_image if self.hovered else self.image, self.rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return self.hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

buttons = [
    Button((225, 160), start_image, start_hover, "PLAY"),
    Button((225, 230), options_image, options_hover, "OPTIONS"),
    Button((225, 300), detail_image, detail_hover, "DETAIL"),
]
launch_game = False

running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(title_image, (125, 40))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        for button in buttons:
            if button.is_clicked(event):
                print(f"{button.action_name} clicked!")
                if button.action_name == "PLAY":
                    launch_game = True
                    running = False
                    pygame.quit()
                    if launch_game:
                        subprocess.Popen(["python", os.path.join("..", "2048", "demo.py")])
                    sys.exit() 

    for button in buttons:
        button.check_hover(mouse_pos)
        button.draw(screen)

    pygame.display.flip()
    clock.tick(60)
