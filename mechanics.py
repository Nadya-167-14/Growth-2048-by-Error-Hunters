import pygame

def mechanics(game):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                game.move("up")
            elif event.key == pygame.K_DOWN:
                game.move("down")
            elif event.key == pygame.K_LEFT:
                game.move("left")
            elif event.key == pygame.K_RIGHT:
                game.move("right")
    return True
