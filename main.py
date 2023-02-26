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

heart = pygame.image.load("assets/heart.png").convert_alpha()

scores = []

def fade(width, height, i):
        fade = pygame.Surface((width, height))
        fade.fill((0, 0, 0))
        
        for alpha in range(0, 300, 2):
            fade.set_alpha(alpha)
            redrawWindow(i)
            screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(1) 
            
        scores.append(level.score)
        text_surface = my_font.render("GAME OVER", False, 'white')
        screen.blit(text_surface, (screen_width / 2.8, screen_width / 12))
        
        text_surface = my_font.render("Score: " + str(level.score), False, 'white')
        screen.blit(text_surface, (screen_width / 2.4, screen_width / 6))
        
        text_surface = my_font.render("High Scores", False, 'white')
        screen.blit(text_surface, (screen_width / 2.7, screen_width / 4))
        
        score_font = pygame.font.SysFont('assets/pixeboy-font/Pixeboy-z8XGD.ttf', 60)
        
        lastPosition = 0
        
        scores_length = len(scores)
        scores.sort()
        for i, n in enumerate(scores[::-1]):
            if i >= 3:
                break
            if n == level.score:
                color = 'gold'
            else:
                color = 'white'
            text_surface = my_font.render(str(i + 1) + ". " + str(n) + " points", False, color)
            screen.blit(text_surface, (screen_width / 2.6, screen_width / 3 + lastPosition))
            lastPosition += 80
            

def redrawWindow(i):    
    bg_img = pygame.image.load(level.bg_img)
    bg_img = pygame.transform.scale(bg_img,(screen_width,screen_height))
    
    screen.fill((0,0,0))
    screen.blit(bg_img,(i,0))
    screen.blit(bg_img,(screen_width+i,0))
    
    if (i == -screen_width):
        screen.blit(bg_img,(screen_width+i,0))
        i=0
    i-=1
    
    level.tiles.update(level.world_shift)
    level.tiles.draw(level.display_surface)
    level.gates.update(level.world_shift)


def main():
    i = 0
    level.lives = 3
    level.score = 0
    
    while True:
        if level.lives <= 0:
            break
        else:
            text_surface = my_font.render(str(level.score), False, 'black')
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
            screen.blit(text_surface, (50,30))
            
            lastPosition = 0
            for j in range(level.lives):
                screen.blit(heart, (20 + lastPosition, 100))
                lastPosition += 40 
        pygame.display.update()
    playAgain(i)
        
def playAgain(i):
    fade(screen_width, screen_width, i)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                level.reset()
                main()
        pygame.display.update()
        clock.tick(60)
                    
        
main()
