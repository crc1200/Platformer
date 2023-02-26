import pygame
from support import import_folder
from level import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.07
        self.image = self.animations['germanRunning'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.size = self.image.get_size()

        #player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 5
        self.gravity = 0.5
        self.jump_speed = -14

        # player status
        self.status = 'germanRunning'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        # transformation 
        self.transform_cool_down = 100
        self.transform_time = 0
        
        # dog dash 
        self.dash_cool_down = 1000
        self.dash_time = 0

        # flying
        self.flying = False
        self.flying_speed = -4
        self.flying_gravity = 0.15
        
        self.death_cooldown = 1000
        self.death_time = 0
        self.lives = 3

    def import_character_assets(self):
        character_path = './graphics/character/'
        self.animations = {'germanIdle': [], 'germanRunning': [],'duck': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]: 
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_LSHIFT]:
            if not self.flying:
                self.dash()
        elif keys[pygame.K_RETURN]:
            self.transform()
        else:
            self.direction.x = 0
        
        if keys[pygame.K_SPACE] and self.on_ground or keys[pygame.K_SPACE] and self.flying:
            self.jump() 
        
        

        

        
            # self.create_jump_particles(self.rect.midbottom)

    def get_status(self):   
        if self.direction.y < 0:
            self.status = 'germanRunning'
        elif self.direction.y > 1:
            self.status = 'germanRunning'
        else:
            if self.direction.x != 0:
                self.status = 'germanRunning'
            else:
                self.status = 'germanRunning'
        if self.flying:
            self.status = 'duck'

    def animate(self):
        animation = self.animations[self.status]

        # loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]

        if self.flying:
            image = pygame.transform.scale(image, (int(self.size[0]*.75), int(self.size[1]*.88)))
        else:
            image = pygame.transform.scale(image, (int(self.size[0]*1.2), int(self.size[1]*1.2)))
        if not self.facing_right:
            self.image = image
        else:
            self.animation_speed = .1
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image

        # set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def apply_gravity(self):
        if self.flying:
            self.direction.y += self.flying_gravity
        else:
            self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        if self.flying:
            self.direction.y = self.flying_speed
        else:
            self.direction.y = self.jump_speed
    def dash(self):
        if pygame.time.get_ticks() - self.dash_time >= self.dash_cool_down:     
                self.direction.x += 10  
                self.dash_time = pygame.time.get_ticks()

    def transform(self):
        if pygame.time.get_ticks() - self.transform_time >= self.transform_cool_down:     
                self.flying = not self.flying          
                self.transform_time = pygame.time.get_ticks()
        

    # def color_change(self):
    #     if self.flying:
    #         self.image.fill('blue')
    #     else:
    #         self.image.fill('red')

    def update(self):
        # self.color_change()
        self.get_input()
        self.get_status()
        self.animate()
        # self.run_dust_animation()


#