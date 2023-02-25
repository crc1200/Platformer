import pygame
from tiles import *
from settings import tile_size, screen_width
from player import Player
import random
from random import *

from support import *


class Level:
    def __init__(self, level_data, surface):

        # level setup
        self.level_data = level_data
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
        self.bg_img = 'assets/trees.png'
        
        self.obstacle_cool_down = 300
        self.obstacle_time = 0
        
        self.world_shift_cool_down = 300
        self.world_shift_time = 0

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        self.score = 0
        
        self.death_cooldown = 1000
        self.death_time = 0
        self.lives = 3

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        # create a group of "gates"
        self.gates = pygame.sprite.Group()
        
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y), self.display_surface)
                    self.player.add(player_sprite)
                if cell == 'T':
                    tile = Gate((x, y), 10, tile_size)
                    self.gates.add(tile)

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x            
            
        if player_x < screen_width / 4 and direction_x < 0:
            player.speed = 0
        if player_x > screen_width - (screen_width / 6) and direction_x > 0:
            player.speed = 0
        else:
            player.speed = 8
            
    def increase_speed(self):
        if pygame.time.get_ticks() - self.death_time >= self.death_cooldown:
            self.world_shift = -(pygame.time.get_ticks()**(1/7))
            self.score = int((pygame.time.get_ticks()/1000) + 2**(pygame.time.get_ticks()/10000)) 
        
    def horizontal_movement_collision(self):
        player = self.player.sprite
        if player.flying:
            player.rect.x += player.direction.x * (player.speed * 0.5)
        else:
            player.rect.x += player.direction.x * (player.speed * 1.3)

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if not self.player.sprite.facing_right:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif self.player.sprite.facing_right:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        for sprite in self.gates.sprites():
            if sprite.rect.colliderect(player.rect):
                if pygame.time.get_ticks() - player.transform_time >= player.transform_cool_down:
                    player.flying = not player.flying
                    if self.bg_img == 'assets/mountains.png':
                        self.bg_img = 'assets/trees.png'
                    else:
                        self.bg_img = 'assets/mountains.png';                
                
                player.transform_time = pygame.time.get_ticks()

                

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def add_obstacles(self):
        if pygame.time.get_ticks() - self.obstacle_time >= self.obstacle_cool_down:
            # numRows = randint(3, 6)
                    
            # for j in range(numRows):
            #     x = randint(1, 11)
            #     y = randint(3, 5)
            #     for i in range(y):
            #         tile = Tile((screen_width + (i * tile_size), x * 109), tile_size)
            #         self.tiles.add(tile)
            
            row_index = randint(1, len(self.level_data) - 1)
            col_index = randint(1, len(self.level_data[0]))
            
            x = screen_width + (col_index * tile_size)
            y = row_index * tile_size
            test = randint(1, 5)
            for i in range(test):
                tile = Tile((x + (i * tile_size), y), tile_size)
                self.tiles.add(tile)
            # tile = Tile((screen_width + (i * tile_size), x * 109), tile_size)
            
            self.obstacle_time = pygame.time.get_ticks()

    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False          
        

    def fade(self, width, height):
            fade = pygame.Surface((width, height))
            fade.fill((0, 0, 0))
            
            for alpha in range(0, 300):
                fade.set_alpha(alpha)
                # self.redrawWindow()
                self.display_surface.blit(fade, (0, 0))
                pygame.display.update()
                pygame.time.delay(1) 

    def redrawWindow(self):
        self.display_surface.fill((255,255,255))
        pygame.draw.rect(self.display_surface, (255, 0, 0), (200, 300, 200, 200), 0)
        pygame.draw.rect(self.display_surface, (0, 255, 0), (200, 300, 200, 200), 0)

    def check_game_over(self):
        player = self.player.sprite
        if (player.rect.x < 0 - player.size[0] or player.rect.y > 1200) and pygame.time.get_ticks() - self.death_time >= self.death_cooldown:
            if self.lives:
                print("CLOSE ONE")
                print(self.lives)
                self.lives -= 1
                self.world_shift = 0
                player.rect.x = screen_width / 4
                player.rect.y = screen_width / 4
                
                flipped_image = pygame.transform.flip(player.image, True, False)
                player.image = flipped_image
            else:
                print("GAME OVER")
            self.death_time = pygame.time.get_ticks()

    def run(self):

        # level tiles
        self.add_obstacles()
        self.increase_speed()
        
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.scroll_x()
        
        # gate tiles
        self.gates.update(self.world_shift)
        # self.gates.draw(self.display_surface)

        # player
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        
        self.check_game_over()
        
    #       self.create_landing_dust()
        self.player.draw(self.display_surface)
