import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        self.animations = {}
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.07
        self.image = self.animations['wolfIdle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)

        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        #self.image = pygame.transform.scale(self.image, (int(self.size[0]*4), int(self.size[1]*4)))
        # draw bigger image to screen at x=100 y=100 position

        #player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'wolfIdle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        
        # transformation 
        self.transform = False
        self.transform_cool_down = 100
        self.transform_time = 0

        # flying
        self.flying = False
        self.flying_speed = -7
        self.flying_gravity = 0.5

    def import_character_assets(self):
        character_path = './graphics/character/'
        #self.animations = {'wolfIdle': [], 'wolfRun': [], 'jump': [], 'fall': [], 'duck': []}
        self.animations = {'wolfIdle': [], 'wolfRun': [], 'wolfJump': [], 'duck': []}

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
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_RETURN]:
            self.flying = True
        if keys[pygame.K_TAB]:
            self.flying = False

        if keys[pygame.K_SPACE] and self.on_ground or keys[pygame.K_SPACE] and self.flying:
            self.jump()
            # self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'wolfJump'
        elif self.direction.y > 1:
            self.status = 'wolfJump'
        else:
            if self.direction.x != 0:
                self.status = 'wolfRun'
            else:
                self.status = 'wolfIdle'
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
            image = pygame.transform.scale(image, (int(self.size[0]*1.25), int(self.size[1]*1.25)))
        else:
            image = pygame.transform.scale(image, (int(self.size[0]*2), int(self.size[1]*2)))
        if not self.facing_right:
            self.image = image
        else:
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