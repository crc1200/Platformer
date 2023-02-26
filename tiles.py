import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, size):
		super().__init__()
		self.image = pygame.Surface((size, size))
		self.rect = self.image.get_rect(topleft = pos)


	def update(self, x_shift):
		self.rect.x += x_shift

class OtherTile(pygame.sprite.Sprite):
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        self.rect.x += shift

  
class Gate(pygame.sprite.Sprite):
    def __init__(self, pos, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect(topleft=pos)
    def update(self, x_shift):
      self.rect.x += x_shift

class StaticTile(OtherTile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface
    def update(self, x_shift):
        self.rect.x += x_shift

class AnimatedTile(OtherTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.05
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size[0] * 4.5), int(size[1] * 4.5)))
        self.image = pygame.transform.flip(self.image, True, False)

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class PowerAnimated(OtherTile):
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.05
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]
        size = self.image.get_size()
        self.image = pygame.transform.scale(self.image, (int(size[0] * 3), int(size[1] * 3)))
        #self.image = pygame.transform.flip(self.image, True, False)

    def update(self, shift):
        self.animate()
        self.rect.x += shift

class DecorTile(OtherTile):
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface
    def update(self, x_shift):
        self.rect.x += x_shift