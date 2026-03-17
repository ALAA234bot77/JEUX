import pygame

# create a class to represent the moving bird enemy
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dmg = 1

        # self.image = pygame.image.load('asset/')
        self.rect = self.image.get_rect()



    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity
