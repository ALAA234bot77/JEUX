import pygame

# create a class to represent the moving bird enemy
class Bird(pygame.sprite.Sprite):
    def __init__(self, game, x=0, y=0, velocity=4):
        super().__init__()
        self.game = game

        self.image = pygame.image.load('asset/seagull test.png')
        self.rect = self.image.get_rect()

        self.world_x = x
        self.world_y = y

        self.rect.x = int(self.world_x)
        self.rect.y = int(self.world_y)



    def move_right(self):

        self.world_x += self.velocity

    def move_left(self):
        self.world_x -= self.velocity

    def sync_rect(self, camera_x=0, camera_y=0):
        self.rect.x = int(self.world_x - camera_x)
        self.rect.y = int(self.world_y - camera_y)


