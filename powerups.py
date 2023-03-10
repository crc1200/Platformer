import pygame
from tiles import AnimatedTile, PowerAnimated
from random import randint

class Powerup(PowerAnimated):
    def __init__(self, size, x, y,):
        super().__init__(size, x, y, './graphics/powerup/wisp')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(1, 3)

    def move(self):
        self.rect.x -= self.speed/2

    # def reverse_image(self):
    #     if self.speed > 0:
    #         self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        # self.reverse_image()
