import pygame

# create a class to represent the player
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dmg = 1




    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity
