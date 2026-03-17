import pygame

class Trash(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((139, 90, 43))  
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = 690  
