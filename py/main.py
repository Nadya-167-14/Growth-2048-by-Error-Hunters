import pygame
from game import Game2048
from ui import draw_game, draw_game_over
from mechanics import mechanics
from menu import show_menu 

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
    draw_game(screen, game)
    draw_score(screen, game.score)

    if game.is_game_over():
        draw_game_over(screen)
        game_over = True

    pygame.display.flip()

    if not game_over:
        running = mechanics(game)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    clock.tick(60)

pygame.quit()
