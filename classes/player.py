import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.health = 3
        self.max_health = 3
        self.velocity = 5

        # Cat image
        self.base_image = pygame.image.load('asset/perso/cat_stand_left.png')
        self.base_image = pygame.transform.scale(self.base_image, (150, 150))

        self.image = self.base_image

        self.rect = self.image.get_rect()
        self.health_image = pygame.image.load('asset/3_hearts.png')

        self.gravity = 0.5
        self.jump_height = -12
        self.jump_velocity = 0
        self.on_ground = True

        # Position in the full world (not screen)
        self.world_x = 515
        self.world_y = 2 * 720 + 540  # near bottom of bottom row

        # track the cat facing left or right
        self.facing = "left"

    def set_facing(self, direction):
        # It is more ecological to do this than make a new png in the asset file
        # Only update if the direction actually changed (avoids flipping every frame)
        if direction == self.facing:
            return

        self.facing = direction  # Remember the new direction

        if direction == "right":
            # Flip horizontally (True) but not vertically (False)
            self.image = pygame.transform.flip(self.base_image, True, False)
        else:
            # Back to the original left-facing image
            self.image = self.base_image

    def update_health_bar(self):
        if self.health == 3:
            self.health_image = pygame.image.load('asset/3_hearts.png')
        elif self.health == 2:
            self.health_image = pygame.image.load('asset/2_hearts.png')
        elif self.health == 1:
            self.health_image = pygame.image.load('asset/1_heart.png')
        else:
            self.health_image = pygame.image.load('asset/no_hearts.png')


    def move_right(self):
        self.world_x += self.velocity
        self.set_facing("right")

    def move_left(self):
        self.world_x -= self.velocity
        self.set_facing("left")

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