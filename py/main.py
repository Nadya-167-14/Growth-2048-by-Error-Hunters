import pygame
import sys
from game import Game2048
from ui import draw_game
from menu import show_menu
import mechanics

# Inisialisasi Pygame
pygame.init()
pygame.display.set_caption("2048 Growth")

# Konstanta ukuran dan warna
WIDTH, HEIGHT = 500, 600
COLOR_TEXT = (50, 50, 50)
COLOR_MENU_BTN = (200, 180, 100)
COLOR_MENU_TEXT = (0, 0, 0)

# Setup screen dan clock
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Font global
font_score = pygame.font.SysFont(None, 36)
font_menu = pygame.font.SysFont(None, 28)

def draw_score(screen, score):
    score_text = font_score.render(f"Score: {score}", True, COLOR_TEXT)
    screen.blit(score_text, (20, 10))

def draw_menu_button(screen):
    menu_rect = pygame.Rect(WIDTH - 120, 10, 100, 40)
    pygame.draw.rect(screen, COLOR_MENU_BTN, menu_rect, border_radius=8)
    menu_text = font_menu.render("Menu", True, COLOR_MENU_TEXT)
    text_rect = menu_text.get_rect(center=menu_rect.center)
    screen.blit(menu_text, text_rect)

def main():
    show_menu(screen)
    game = Game2048()
    running = True

    while running:
        screen.fill((250, 248, 239))
        draw_game(screen, game)
        draw_score(screen, game.score)
        draw_menu_button(screen)

        pygame.display.flip()
        running = mechanics.mechanics(game)
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
