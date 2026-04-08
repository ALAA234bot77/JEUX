import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width=200, height=40):
        # Initialize the pygame Sprite base class
        super().__init__()

        # Load the platform and well-size it
        original_image = pygame.image.load('asset/platform/pf_1.png')
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()

        # Place the platform at given coordinates x and y
        self.rect.x = x
        self.rect.y = y



class MovingPlatform(Platform):
    def __init__(self, game, x, y, target_x, target_y, speed=2, width=200, height=40):
        # Initialize the parent Platform at the starting position
        super().__init__(game, x, y, width, height)

        # Starting point
        self.start_x = float(x)
        self.start_y = float(y)

        # Target point
        self.target_x = float(target_x)
        self.target_y = float(target_y)

        self.speed = speed  # Pixels per frame

        # Current position as floats for smooth !
        self.world_x = float(x)
        self.world_y = float(y)

        # Direction vector
        dx = self.target_x - self.start_x
        dy = self.target_y - self.start_y
        length = (dx**2 + dy**2) ** 0.5    # Euclidean distance between the two points :D

        # Avoid division by zero if start == target
        if length == 0:
            self.dir_x = 0.0
            self.dir_y = 0.0
        else:
            self.dir_x = dx / length
            self.dir_y = dy / length

        # 1 = moving toward target
        self.direction = 1

    def update(self):
        # Save position before moving so we can compute displacement
        prev_x = self.world_x
        prev_y = self.world_y

        # Move the platform along its direction vector
        self.world_x += self.dir_x * self.speed * self.direction
        self.world_y += self.dir_y * self.speed * self.direction

        # Check if we've reached (or passed) the target or start
        total_length = ((self.target_x - self.start_x)**2 + (self.target_y - self.start_y)**2) ** 0.5
        traveled = ((self.world_x - self.start_x) * self.dir_x +
                    (self.world_y - self.start_y) * self.dir_y)

        if self.direction == 1 and traveled >= total_length:
            # Reached the target — snap to it and reverse
            self.world_x = self.target_x
            self.world_y = self.target_y
            self.direction = -1

        elif self.direction == -1 and traveled <= 0:
            # Reached the start — snap to it and reverse
            self.world_x = self.start_x
            self.world_y = self.start_y
            self.direction = 1

        # Sync the rect to the new world position
        self.rect.x = int(self.world_x)
        self.rect.y = int(self.world_y)

        # This will be used by game.py to carry the player along
        self.delta_x = self.world_x - prev_x
        self.delta_y = self.world_y - prev_y