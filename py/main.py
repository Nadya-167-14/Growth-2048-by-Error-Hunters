import pygame
from game import Game2048
from ui import draw_game, draw_game_over
from mechanics import mechanics
from menu import show_menu 
from powerup import pupuk, penyiram_otomatis, bom

COLOR_TEXT = (50, 50, 50)

pygame.init()
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Growth 2048")

font_score = pygame.font.SysFont(None, 36)
font_menu = pygame.font.SysFont(None, 28)

def draw_score(screen, score):
    score_text = font_score.render(f"Score: {score}", True, COLOR_TEXT)
    screen.blit(score_text, (20, 10))

show_menu(screen)

game = Game2048()
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    screen.fill((250, 246, 227))

    powerup_buttons = draw_game(screen, game)
    draw_score(screen, game.score)

    if game.is_game_over():
        draw_game_over(screen)
        game_over = True

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if not game_over:
                if powerup_buttons[0].collidepoint(mouse_pos):
                    pupuk(game, 0, 0) 
                elif powerup_buttons[1].collidepoint(mouse_pos):
                    penyiram_otomatis(game)
                elif powerup_buttons[2].collidepoint(mouse_pos):
                    bom(game, 0, 0) 

    if not game_over:
        running = mechanics(game)

    clock.tick(60)

pygame.quit()
