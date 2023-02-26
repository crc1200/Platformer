import pygame

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
