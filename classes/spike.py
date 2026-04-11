import pygame


class spike(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        original_image = pygame.image.load('asset/perso_67.png')
        self.image = pygame.transform.scale(original_image, (50, 50))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.bottom = y
        self.immunity = False
