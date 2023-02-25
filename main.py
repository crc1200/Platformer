import pygame, sys
from settings import *
from level import *

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

i = 0
while True:
    bg_img = pygame.image.load(level.bg_img)
    bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height))
    screen.fill((0,0,0))
    screen.blit(bg_img,(i,0))
    screen.blit(bg_img,(screen_width+i,0))
    if (i==-screen_width):
        screen.blit(bg_img,(screen_width+i,0))
        i=0
    i-=1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    level.run()
    pygame.display.update()
    clock.tick(60)