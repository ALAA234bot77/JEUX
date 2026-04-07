import pygame

# create a class to represent the moving bird enemy
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


        self.image = pygame.image.load('asset/')
        self.rect = self.image.get_rect()




