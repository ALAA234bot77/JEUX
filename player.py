import pygame

# create a class to represent the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.velocity = 5
        self.image = pygame.image.load('asset/perso_67.webp')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = 515
        self.rect.y =690


        self.gravity= 0.5
        self.jump_height= -12
        self.jump_velocity= 0
        self.on_ground = True
        self.ground = 690
        self.rect.bottom = self.ground




    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def jump(self):
        if self.on_ground:
            self.jump_velocity = self.jump_height
            self.on_ground = False

    def apply_gravity(self):
        self.jump_velocity += self.gravity
        self.rect.y += self.jump_velocity

        #stop at ground
        if self.rect.bottom >= self.ground:
            self.rect.bottom = self.ground
            self.jump_velocity = 0
            self.on_ground = True