import pygame
from game import Game2048
from ui import draw_game, draw_game_over, init_ui_assets, _ui_assets, draw_game_won
from menu import show_menu
from powerup import PupukPowerUp, PenyiramOtomatisPowerUp, BomPowerUp, active_animations
from animation import BombAnimation, PupukAnimation
from details import detail_menu
import os

COLOR_TEXT = (50, 50, 50)

pygame.init()
pygame.mixer.init()
pygame.font.init()
screen_width, screen_height = 500, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Growth 2048")

init_ui_assets()
font_score = pygame.font.SysFont(None, 36)
game_over_sfx = pygame.mixer.Sound("assets/sfx/gameover.mp3")
game_won_sfx = pygame.mixer.Sound("assets/sfx/win.mp3")

def draw_score(screen, score):
    font_pixel = _ui_assets["font_pixel_small"]
    score_text = font_pixel.render(f"Score: {score}", True, COLOR_TEXT)
    score_x = 20
    score_y = screen.get_height() - 100
    screen.blit(score_text, (score_x, score_y))

def add_bomb_animation(row, col):
    x = col * 100 + 20
    y = row * 100 + 20
    anim = BombAnimation((x, y))
    active_animations.append(anim)

def add_pupuk_animation(row, col):
    x = col * 100 + 20
    y = row * 100 + 20
    anim = PupukAnimation((x, y))
    active_animations.append(anim)

import powerup
powerup.add_bomb_animation = add_bomb_animation
powerup.add_pupuk_animation = add_pupuk_animation

def run_game():
    game = Game2048(screen_width, screen_height)
    game_over = False
    game_won = False
    game_over_sound_played = False
    game_won_sound_played = False
    clock = pygame.time.Clock()

    while True:
        screen.fill((250, 246, 227))

        powerup_buttons = draw_game(screen, game)
        draw_score(screen, game.score)

        dt = clock.tick(60)
        for anim in active_animations[:]:
            try:
                anim.update(dt)
            except TypeError:
                anim.update()
            anim.draw(screen)
            if hasattr(anim, "finished") and anim.finished:
                active_animations.remove(anim)
            elif hasattr(anim, "active") and not anim.active:
                active_animations.remove(anim)

        menu_button_rect = None

        if game.is_game_over():
            menu_button_rect = draw_game_over(screen)
            game_over = True
            if not game_over_sound_played:
                game_over_sfx.play()
                game_over_sound_played = True
        elif game.has_won():
            menu_button_rect = draw_game_won(screen)
            game_won = True
            if not game_won_sound_played:
                game_won_sfx.play()
                game_won_sound_played = True

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif not game_over and not game_won:
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
                if (game_over or game_won) and menu_button_rect and menu_button_rect.collidepoint((mouse_x, mouse_y)):
                    return True
                if not game_over and not game_won:
                    if game.active_powerup is None:
                        if powerup_buttons[0].collidepoint((mouse_x, mouse_y)):
                            game.active_powerup = 'pupuk'
                        elif powerup_buttons[1].collidepoint((mouse_x, mouse_y)):
                            PenyiramOtomatisPowerUp(game).activate()
                        elif powerup_buttons[2].collidepoint((mouse_x, mouse_y)):
                            game.active_powerup = 'bom'
                    else:
                        row, col = game.get_board_coords((mouse_x, mouse_y))
                        if row is not None and col is not None:
                            if game.active_powerup == 'pupuk':
                                PupukPowerUp(game).activate(row, col)
                            elif game.active_powerup == 'bom':
                                BomPowerUp(game).activate(row, col)
                            game.active_powerup = None
                        else:
                            game.active_powerup = None

running = True
while running:
    show_menu(screen)
    running = run_game()

pygame.quit()
