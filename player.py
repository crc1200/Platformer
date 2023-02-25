# import pygame
# from level import *
#
#
# class Player(pygame.sprite.Sprite):
#     def __init__(self, pos, surface):
#         super().__init__()
#         self.image = pygame.Surface((45, 45))
#         self.image.fill('red')
#         self.rect = self.image.get_rect(topleft=pos)
#
#         # player movement
#         self.direction = pygame.math.Vector2(0, 0)
#         self.speed = 8
#         self.gravity = 0.8
#         self.jump_speed = -16
#
#         # flying mechanics
#         self.flying_time = None
#         self.flying = False
#         self.flying_speed = -7
#         self.flying_gravity = 0.5
#         self.flap_cooldown = 800
#
#         # player status
#         # self.status = 'idle'
#         # self.facing_right = True
#         # self.on_ground = False
#         # self.on_ceiling = False
#         # self.on_left = False
#         # self.on_right = False
#
#     # def get_input(self):
#     #     keys = pygame.key.get_pressed()
#     #
#     #     if keys[pygame.K_RIGHT]:
#     #         self.direction.x = 1
#     #         #self.facing_right = True
#     #     elif keys[pygame.K_LEFT]:
#     #         self.direction.x = -1
#     #         #self.facing_right = False
#     #     else:
#     #         self.direction.x = 0
#     #     # if keys[pygame.K_RETURN]:
#     #     #     self.flying = True
#     #     # if keys[pygame.K_TAB]:
#     #     #     self.flying = False
#     #
#     #     if keys[pygame.K_SPACE]:
#     #         self.jump()
#     #     # if keys[pygame.K_SPACE] and self.flying:
#     #     #     self.flying_time = pygame.time.get_ticks()
#     #     #     if self.fly_cooldown():
#     #     #         self.jump()
#
#     def get_input(self):
#         keys = pygame.key.get_pressed()
#
#         if keys[pygame.K_RIGHT]:
#             self.direction.x = 1
#             #self.facing_right = True
#         elif keys[pygame.K_LEFT]:
#             self.direction.x = -1
#             #self.facing_right = False
#         else:
#             self.direction.x = 0
#
#         if keys[pygame.K_SPACE]:
#             self.jump()
#
#     def get_status(self):
#         if self.direction.y < 0:
#             self.status = 'jump'
#         elif self.direction.y > 1:
#             self.status = 'fall'
#         else:
#             if self.direction.x != 0:
#                 self.status = 'run'
#             else:
#                 self.status = 'idle'
#
#     def apply_gravity(self):
#         if self.flying:
#             self.direction.y += self.flying_gravity
#         else:
#             self.direction.y += self.gravity
#         self.rect.y += self.direction.y
#
#     def jump(self):
#         if self.flying:
#             self.direction.y = self.flying_speed
#         else:
#             self.direction.y = self.jump_speed
#
#     # def color_change(self):
#     #     if self.flying:
#     #         self.image.fill('blue')
#     #     else:
#     #         self.image.fill('red')
#     #
#     # def fly_cooldown(self):
#     #     current_time = pygame.time.get_ticks()
#     #     if current_time - self.flying_time >= self.flap_cooldown:
#     #         return False
#     #     else:
#     #         return True
#
#     def update(self):
#         # self.color_change()
#         self.get_input()
#
#         self.get_status()

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        # self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        # self.image = self.animations['idle'][self.frame_index]
        self.image = pygame.Surface((45, 45))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16

        # player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

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

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            # self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.get_input()
        self.get_status()
        # self.animate()
        # self.run_dust_animation()
