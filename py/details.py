import pygame
import sys
from ui import get_font

pygame.init()

WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Details")


background = pygame.image.load("assets/bg_details.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

font_title = get_font("font_pixel_small") 
font_body = pygame.font.Font("assets/fonts/pressstart2p.ttf", 10)  

lines = [
    "DIBUAT OLEH:",
    "Kelompok Error Hunters",
    "- Nadya Shafwah Yusuf",
    "  123140167",
    "- Fadina Mustika",
    "  Ratnaningsih"
    "  123140157",
    "- Bulan Nindya Sapta Putri",
    "  120140231",
    "- M. Farhan Muzakhi",
    "  123140075",
    "- Punky Wijayanto Muda",
    "  119140088",
    "",
    "Tekan ESC untuk kembali ke menu."
]

def draw_detail():
    screen.blit(background, (0, 0))

    y = 100
    padding_x = 40  
    for line in lines:
        text = font_body.render(line, True, (0, 0, 0))
        screen.blit(text, (padding_x, y))
        y += 20 

    pygame.display.flip()

def detail_menu():
    running = True
    while running:
        draw_detail()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
