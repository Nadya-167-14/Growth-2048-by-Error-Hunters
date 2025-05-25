import pygame
from game import Game2048
from ui import draw_game, draw_game_over, init_ui_assets
from mechanics import mechanics_logic 
from menu import show_menu
from powerup import pupuk, penyiram_otomatis, bom

COLOR_TEXT = (50, 50, 50)

pygame.init()
pygame.font.init() 
screen_width, screen_height = 500, 600 
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Growth 2048")

init_ui_assets() 

font_score = pygame.font.SysFont(None, 36)

def draw_score(screen, score):
    score_text = font_score.render(f"Score: {score}", True, COLOR_TEXT)
    score_x = (screen_width - score_text.get_width()) // 2
    score_y = 50 
    screen.blit(score_text, (score_x, score_y))

show_menu(screen)

game = Game2048(screen_width, screen_height) 
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
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif not game_over:
                if event.key == pygame.K_UP:
                    game.move("up")
                elif event.key == pygame.K_DOWN:
                    game.move("down")
                elif event.key == pygame.K_LEFT:
                    game.move("left")
                elif event.key == pygame.K_RIGHT:
                    game.move("right")
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            if not game_over:
                if game.active_powerup is None:
                    if powerup_buttons[0].collidepoint((mouse_x, mouse_y)):
                        game.active_powerup = 'pupuk'
                        print("Pupuk dipilih. Klik di papan untuk menggunakannya.")
                    elif powerup_buttons[1].collidepoint((mouse_x, mouse_y)):
                        penyiram_otomatis(game)
                        game.active_powerup = None
                    elif powerup_buttons[2].collidepoint((mouse_x, mouse_y)):
                        game.active_powerup = 'bom'
                        print("Bom dipilih. Klik di papan untuk meledakkannya.")
                else:
                    row, col = game.get_board_coords((mouse_x, mouse_y))
                    
                    if row is not None and col is not None:
                        if game.active_powerup == 'pupuk':
                            pupuk(game, row, col)
                        elif game.active_powerup == 'bom':
                            bom(game, row, col)
                        
                        game.active_powerup = None
                    else:
                        print("Klik di luar papan, batalkan pemilihan power-up.")
                        game.active_powerup = None

    if not game_over:
        running = mechanics_logic(game) 

    clock.tick(60)

pygame.quit()
