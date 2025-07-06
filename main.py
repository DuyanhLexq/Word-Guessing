import pygame
import consts
pygame.init()

pygame.display.set_caption(consts.GAME_CAPTION)
screen = pygame.display.set_mode((consts.SCREEN_WIDTH, consts.SCREEN_HEIGHT))
game_play = True
clock = pygame.time.Clock()

while game_play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_play = False
    
    screen.fill(consts.DEFAULT_BACKGROUND_COLOR)
    pygame.display.update()
    clock.tick(consts.FPS)
    