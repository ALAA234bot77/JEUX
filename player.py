import pygame

# create a class to represent the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.velocity = 1
        self.image = pygame.image.load('asset/perso_67.webp')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y =300


    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity
