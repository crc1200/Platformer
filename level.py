import pygame
from tiles import *
from settings import tile_size, screen_width
from player import Player
import random
from random import *
from support import *

class Level:
    def __init__(self, level_data, surface):
        self.t = self.import_terrain()
        # level setup
        self.level_data = level_data
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0
        self.bg_img = 'assets/trees.png'
        
        self.obstacle_cool_down = 500
        self.obstacle_time = 0

        self.floor_cool_down = 300
        self.floor_time = 0
        
        self.world_shift_cool_down = 800
        self.world_shift_time = 0

        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
        self.score = 0
        
        self.death_cooldown = 1000
        self.death_time = 0
        self.lives = 3
        
        self.time = 0

        # images


    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def import_terrain(self):
        i = 0
        terrain_path = './graphics/terrain/'
        t = {'island1': [], 'island3': [], 'island4': [], 'doubleLeft': [], 'doubleRight': [], 'regular': [], 'single': [], 'middle': []}

        for tey in t.keys():
            print(tey)
            i += 1
            full_path = terrain_path + tey
            t[tey] = import_folder(full_path)

        return t

    def setup_level(self, layout):
        
        self.time = pygame.time.get_ticks()
        
        self.tiles = pygame.sprite.Group()
        # create a group of "gates"
        self.gates = pygame.sprite.Group()
        
        self.player = pygame.sprite.GroupSingle()

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if cell == 'X':
                    block = self.t['regular']
                    #for i in range(3):
                    t = randint(0, 2)

                    image = block[t]
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                    tile = StaticTile(tile_size, x + (tile_size), y, image)
                    self.tiles.add(tile)
                    self.tiles.add(tile)
                if cell == 'Q':
                    block = self.t['doubleLeft']
                    image = block[0]
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                    tile = StaticTile(tile_size, x + (tile_size), y, image)
                    self.tiles.add(tile)
                if cell == 'W':
                    block = self.t['doubleRight']
                    image = block[0]
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                    tile = StaticTile(tile_size, x + (tile_size), y, image)
                    self.tiles.add(tile)
                if cell == 'S':
                    image = pygame.image.load('./graphics/terrain/mainSingle.png').convert_alpha()
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                    tile = StaticTile(tile_size, x + (tile_size), y, image)
                    self.tiles.add(tile)
                if cell == 'P':
                    print(x, y)
                    player_sprite = Player((x, y), self.display_surface)
                    self.player.add(player_sprite)
                if cell == 'T':
                    tile = Gate((x, y), 10, tile_size)
                    self.gates.add(tile)
                if cell == 'M':
                    block = self.t['middle']
                    #for i in range(3):
                    t = randint(0, 2)

                    image = block[t]
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                    tile = StaticTile(tile_size, x + (tile_size), y, image)
                    self.tiles.add(tile)
                    self.tiles.add(tile)

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
        if pygame.time.get_ticks() - self.world_shift_time >= self.world_shift_cool_down:
            self.world_shift = -((pygame.time.get_ticks() - self.time)**(1/10))
            self.score = int(((pygame.time.get_ticks() - self.time) /1000) + 2**((pygame.time.get_ticks() - self.time)/10000)) 
            self.world_shift_time = pygame.time.get_ticks()
        
    def horizontal_movement_collision(self):
        player = self.player.sprite
        if player.flying:
            player.rect.x += player.direction.x * (player.speed * 0.3)
        else:
            player.rect.x += player.direction.x * (player.speed * 0.8)

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
            inner = pygame.sprite.Group()
            # row_index = randint(1, len(self.level_data) - 1)
            col_index = randint(1, len(self.level_data[0]))
            row_index = randint(1, 6)
            col_index = randint(1, 7)
            
            x = screen_width + (col_index * tile_size)
            y = row_index * tile_size
            test = randint(1, 3)

            if test == 1:
                image = pygame.image.load('./graphics/terrain/mainSingle.png').convert_alpha()
                size = image.get_size()
                image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                tile = StaticTile(tile_size, x + (tile_size), y, image)
                collide = pygame.sprite.spritecollide(tile, self.tiles, True)
                if not collide:
                    inner.add(tile)
            #
            elif test == 2:
                right = self.t['doubleLeft']
                left = self.t['doubleRight']

                
               
                imageRight = right[0]
                size1 = imageRight.get_size()
                imageRight = pygame.transform.scale(imageRight, (int(size1[0] * 5), int(size1[1] * 5)))
                tileRight = StaticTile(tile_size, x , y, imageRight)
                collideRight = pygame.sprite.spritecollide(tileRight, self.tiles, True)
                if not collideRight:
                    inner.add(tileRight)
                
                imageLeft = left[0]
                size1 = imageLeft.get_size()
                imageLeft = pygame.transform.scale(imageLeft, (int(size1[0] * 5), int(size1[1] * 5)))
                tileLeft = StaticTile(tile_size, x + (tile_size), y, imageLeft)
                collideLeft = pygame.sprite.spritecollide(tileLeft, self.tiles, True)
                if not collideLeft:
                    inner.add(tileLeft)

            elif test == 3:
                block = self.t['island3']
                inner = pygame.sprite.Group()
                for i in range(3):
                    image = block[2 - i]
                    size = image.get_size()
                    image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                    tile = StaticTile(tile_size, x + (i * tile_size), y, image)
                    collide = pygame.sprite.spritecollide(tile, self.tiles, True)
                    if not collide:
                        inner.add(tile)

            # elif test == 4:
            #     block = self.t['island4']
            #     for i in range(4):
            #         image = block[3 - i]
            #         size = image.get_size()
            #         image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
            #         tile = StaticTile(tile_size, x + (i * tile_size), y, image)
            #         collide = pygame.sprite.spritecollide(tile, self.tiles, True)
            #         if not collide:
            #             inner.add(tile)
            for i in inner:
                self.tiles.add(i)

            
            self.obstacle_time = pygame.time.get_ticks()
    #
    def generate_floor(self):
        if pygame.time.get_ticks() - self.floor_time >= self.floor_cool_down:
            row_indexTop = 7
            row_indexBottom = 8
            lower = pygame.sprite.Group()


            
            x = screen_width + tile_size
            yTop = row_indexTop * tile_size
            

            middleTiles = self.t['middle']
            for i in range(5):
                
                middleInt = randint(0, 2)
                yBottom = (i + row_indexBottom) * tile_size

                image = middleTiles[middleInt]
                size = image.get_size()
                image = pygame.transform.scale(image, (int(size[0] * 5), int(size[1] * 5)))
                middleTile = StaticTile(tile_size, x + tile_size, yBottom, image)
                lower.add(middleTile)

            topTiles = self.t['regular']
            topInt = randint(0, 2)


            image2 = topTiles[topInt]
            size2 = image2.get_size()
            image2 = pygame.transform.scale(image2, (int(size2[0] * 5), int(size2[1] * 5)))
            topTile = StaticTile(tile_size, x + tile_size, yTop, image2)

            self.tiles.add(topTile)
            for l in lower:
                self.tiles.add(l)
            self.floor_time = pygame.time.get_ticks()


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

    def check_game_over(self):
        player = self.player.sprite
        if (player.rect.x < 0 - player.size[0] or player.rect.y > 1200) and pygame.time.get_ticks() - self.death_time >= self.death_cooldown:
            
            self.lives -= 1
            self.world_shift = 0
            
            player.rect.x = screen_width / 4
            player.rect.y = screen_width / 4
            
            flipped_image = pygame.transform.flip(player.image, True, False)
            player.image = flipped_image
            if self.lives == 0:
                self.time = pygame.time.get_ticks()
            self.death_time = pygame.time.get_ticks()
    
    def reset(self):
        player = self.player.sprite
        self.score = 0
        self.setup_level(self.level_data)


    def run(self):
        # level tiles
        self.add_obstacles()
        self.increase_speed()
        self.generate_floor()
        
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
