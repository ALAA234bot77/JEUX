import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y, width=200, height=40):
        super().__init__()

        # Load image first
        original_image = pygame.image.load('asset/platform/pf_1.png')
        # THEN scale it
        self.image = pygame.transform.scale(original_image, (width, height))
        self.rect = self.image.get_rect()

        self.world_x = x
        self.world_y = y

        self.rect.x = int(self.world_x)
        self.rect.y = int(self.world_y)


    def check_collision_with_player(self, player):
        """
        Check if player is colliding with this specific platform.
        Returns True if player lands on this platform.
        """
        player_rect = player.rect.copy()
        player_rect.centerx = int(player.world_x)
        player_rect.bottom = int(player.world_y)

        # Only check if player is falling (moving down)
        if player.jump_velocity > 0:
            # Check if player's feet are touching platform's top
            if (player_rect.bottom >= self.rect.top and
                    player_rect.bottom <= self.rect.top + 10 and
                    player_rect.right > self.rect.left and
                    player_rect.left < self.rect.right):
                return True

        return False

    def land_player(self, player):
        """
        Make the player land on this platform.
        """
        player.world_y = self.rect.top
        player.jump_velocity = 0
        player.on_ground = True

    @staticmethod
    def create_platforms_for_level(game, level=1):
        """
        Static method to create platforms based on level.
        Returns a list of Platform objects.
        """
        platforms = []

        if level == 1:
            platforms_data = [
                (500, 500),
                (1000, 400),
                (1500, 350),
                (2000, 500),
                (800, 250),
            ]
        elif level == 2:
            platforms_data = [
                (500, 500),
                (1000, 400),
                (1500, 350),
                (2000, 500),
                (800, 250),
                (1200, 600),
                (2500, 300),
            ]
        elif level == 3:
            platforms_data = [
                (500, 500),
                (1000, 400),
                (1500, 350),
                (2000, 500),
                (800, 250),
                (1200, 600),
                (2500, 300),
                (400, 150),
                (2800, 450),
            ]
        else:
            # Default platforms
            platforms_data = [(500, 500)]

        for x, y in platforms_data:
            platforms.append(Platform(game, x=x, y=y))

        return platforms

    @staticmethod
    def check_all_platforms_collision(platforms, player):
        """
        Check collision between player and all platforms.
        Returns True if player landed on any platform.
        """
        for platform in platforms:
            if platform.check_collision_with_player(player):
                platform.land_player(player)
                return True
        return False