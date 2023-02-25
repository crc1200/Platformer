import pygame
from tiles import *
from settings import tile_size, screen_width
from player import Player
import random
from random import *



class Level:
    def __init__(self, level_data, surface):

        # level setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = -4
        self.current_x = 0
        self.bg_img = 'assets/trees.png'

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

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
            self.world_shift = -4
            player.speed = 0
        if player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -4
            player.speed = 0
        else:
            self.world_shift = -4
            player.speed = 8

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

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
                    print(screen_width / tile_size)
                    
                    
                    # player.direction.y = -14
                    
                    # player.flying_speed = -7
                    # player.flying_gravity = 0.2
                    
                    # player.speed = -7
                    # player.gravity = 0.2
                    
                    # self.fade(screen_width, screen_width)
                    # player.direction.y = -14
                    #
                    # player.flying_speed = -7
                    # player.flying_gravity = 0.2
                    #
                    # player.speed = -7
                    # player.gravity = 0.2
                    #
                    # self.fade(screen_width, screen_width)
                
                player.transform_time = pygame.time.get_ticks()
                

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def add_obstacles(self):
        
        print(randint(1, 11))
        print(randint(1, 5))
        
        tile = Tile((screen_width, 100), tile_size)
        self.tiles.add(tile)

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


    def run(self):

        # level tiles
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
        
    #       self.create_landing_dust()
        self.player.draw(self.display_surface)
