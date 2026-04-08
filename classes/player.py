import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 3
        self.max_health = 3
        self.velocity = 5
        self.image = pygame.image.load('asset/perso_67.png')
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.health_image = pygame.image.load('asset/3_hearts.png')

        self.gravity = 0.5
        self.jump_height = -12
        self.jump_velocity = 0
        self.on_ground = True

        # Position in the full world (not screen)
        self.world_x = 515
        self.world_y = 2 * 720 + 540  # near bottom of bottom row

    def update_health_bar(self):
        if self.health == 3:
            self.health_image = pygame.image.load('asset/3_hearts.png')
        elif self.health == 2:
            self.health_image = pygame.image.load('asset/2_hearts.png')
        elif self.health == 1:
            self.health_image = pygame.image.load('asset/1_heart.png')
        else:
            self.health_image = pygame.image.load('asset/0_heart.png')


    def move_right(self):
        """if not self.game.check_collisions (self, self.game.platforms):"""
        self.world_x += self.velocity

    def move_left(self):
        """if not self.game.check_collisions(self, self.game.platforms):"""
        self.world_x -= self.velocity

    def jump(self):
        if self.on_ground:
            self.jump_velocity = self.jump_height
            self.on_ground = False

    def apply_gravity(self, world_h):
        self.jump_velocity += self.gravity
        self.world_y += self.jump_velocity

        # Hard floor at bottom of world
        if self.world_y >= world_h - 30:
            self.world_y = world_h - 30
            self.jump_velocity = 0
            self.on_ground = True