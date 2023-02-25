import pygame, sys
from settings import *
from level import *
from support import *

# Pygame setup
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_map, screen)

i = 0

my_font = pygame.font.SysFont('assets/pixeboy-font/Pixeboy-z8XGD.ttf', 80)

while True:
    text_surface = my_font.render(str(level.score), False, 'white')
    bg_img = pygame.image.load(level.bg_img)
    bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height))
    screen.fill((0,0,0))
    screen.blit(bg_img,(i,0))
    screen.blit(bg_img,(screen_width+i,0))
    if (i == -screen_width):
        screen.blit(bg_img,(screen_width+i,0))
        i=0
    i-=1
    
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    level.run()
    screen.blit(text_surface, (50,30))
    pygame.display.update()
    clock.tick(60)