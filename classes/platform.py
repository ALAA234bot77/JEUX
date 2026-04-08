import pygame

# create a class to represent the solid platform
class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()


        self.image = pygame.image.load('asset/concrete_slab.png')
        self.rect = self.image.get_rect()

        self.world_x = x
        self.world_y = y

        self.rect.x = int(self.world_x)
        self.rect.y = int(self.world_y)


