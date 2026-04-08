from classes.platform import Platform, MovingPlatform
from classes.player import Player
from classes.trash import Trash
from classes.bin import Bin
from classes.birdenemy import Bird
import pygame


# create a class to represent our game
class Game:

    def __init__(self):
        # ← KEPT from old file
        self.all_players = pygame.sprite.Group()

        self.player = Player(self)

        # ← KEPT from old file
        self.all_players.add(self.player)

        self.pressed = {}
        self.score = 0
        self.lives = 3
        self.level = 1
        self.carrying = False
        self.carried_trash_type = None

        self.camera_x = 0
        self.camera_y = 0

        self.all_trash = self.create_trash()
        self.all_bins = self.create_bins()
        self.visible_trash = []

        self.flock = pygame.sprite.Group()
        self.bird_spawn()

        self.platforms = pygame.sprite.Group()
        self.platform_spawn()

    def check_collisions(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)







# ----------------------- TRASH STUFF ----------------------------
    # ------------------------------------------------------ #
    #  TRASH                                                 #
    # ------------------------------------------------------ #
    def create_trash(self):
        if self.level == 1:
            return [
                Trash(800, "recyclable"),
                Trash(1200, "menager"),
                Trash(1600, "recyclable"),
                Trash(2000, "menager"),
            ]
        elif self.level == 2:
            return [
                Trash(800, "recyclable"),
                Trash(1200, "menager"),
                Trash(1600, "compost"),
                Trash(2000, "papier"),
            ]
        elif self.level == 3:
            return [
                Trash(800, "recyclable"),
                Trash(1200, "menager"),
                Trash(1600, "compost"),
                Trash(2000, "papier"),
                Trash(2400, "verre"),
                Trash(2800, "vetement"),
            ]

    def create_bins(self):
        if self.level == 1:
            return [
                Bin(300, "recyclable"),
                Bin(500, "menager"),
            ]
        elif self.level == 2:
            return [
                Bin(300, "recyclable"),
                Bin(500, "menager"),
                Bin(700, "compost"),
                Bin(900, "papier"),
            ]
        elif self.level == 3:
            return [
                Bin(300, "recyclable"),
                Bin(500, "menager"),
                Bin(700, "compost"),
                Bin(900, "papier"),
                Bin(1100, "verre"),
                Bin(1300, "vetement"),
            ]

    def update_trash_visibility_old(self):
        """KEPT from original file"""
        for trash in self.all_trash[:]:
            screen_x = trash.rect.x - self.camera_x
            if -50 < screen_x < 1130:
                if trash not in self.visible_trash:
                    self.visible_trash.append(trash)

            adjusted_rect = trash.rect.move(-self.camera_x, 0)
            if adjusted_rect.colliderect(self.player.rect):
                if not self.carrying:
                    self.all_trash.remove(trash)
                    if trash in self.visible_trash:
                        self.visible_trash.remove(trash)
                    self.carrying = True
                    self.carried_trash_type = trash.trash_type

    # ========== NEW VERSION (currently used) ==========
    def update_trash_visibility(self, screen_w=1080):
        """Keep only trash close enough to appear on screen"""
        self.visible_trash = []
        for trash in self.all_trash:
            screen_x = trash.rect.x - self.camera_x
            if -50 < screen_x < screen_w + 50:
                self.visible_trash.append(trash)

    def try_pickup_trash(self):
        """Pickup trash in world space"""
        if self.carrying:
            return

        player_world_rect = self.player.rect.copy()
        player_world_rect.centerx = int(self.player.world_x)
        player_world_rect.bottom = int(self.player.world_y)

        for trash in self.all_trash[:]:
            if trash.rect.colliderect(player_world_rect):
                self.all_trash.remove(trash)
                if trash in self.visible_trash:
                    self.visible_trash.remove(trash)
                self.carrying = True
                self.carried_trash_type = trash.trash_type
                return

    def throw_trash(self):
        """Throw trash into bin (world space collision)"""
        if not self.carrying:
            return

        player_world_rect = self.player.rect.copy()
        player_world_rect.centerx = int(self.player.world_x)
        player_world_rect.bottom = int(self.player.world_y)

        for bin_obj in self.all_bins:
            if abs(player_world_rect.centerx - bin_obj.rect.centerx) < 100:
                if self.carried_trash_type == bin_obj.bin_type:
                    self.score += 1
                    print(f"✅ Bravo ! Score : {self.score}")
                else:
                    self.lives -= 1
                    print(f"❌ Mauvaise poubelle ! Vies : {self.lives}")

                self.carrying = False
                self.carried_trash_type = None
                return






# ----------------------------- PLATFORM STUFF -----------------------------------
    # ------------------------------------------------------------------ #
    #  Platforms per level — Modify here                                 #
    # ------------------------------------------------------------------ #

    # If you want to add a STATIC platform, simply put his coordinates in a tuple right here. You don't have to modify anything else.
    # If you want to add a MOVING platform, put in a dictionary from which coordinated to which you want it to move
    PLATFORMS_BY_LEVEL = {
        1: [
            (800, 1980),
            (450, 1950),
            (200, 1850),
            {"x": 600, "y": 1700, "target_x": 1100, "target_y": 1700, "speed": 2},
            {"x": 1200, "y": 2000, "target_x": 1200, "target_y": 1300, "speed": 2}
        ],
        2: [
            (800, 1980),

        ],
        3: [
            (800, 1980),

        ]
    }

    def platform_spawn(self):

        # Look up the platform positions for the current level (liste vide si niveau inconnu)
        positions = self.PLATFORMS_BY_LEVEL.get(self.level, [])

        for entry in positions:
            if isinstance(entry, tuple):
                x, y = entry
                platform = Platform(self, x=x, y=y)
            elif isinstance(entry, dict):
                # Moving platform — unpack all parameters from the dict
                platform = MovingPlatform(
                    self,
                    x=entry["x"],
                    y=entry["y"],
                    target_x=entry["target_x"],
                    target_y=entry["target_y"],
                    speed=entry.get("speed", 2),  # Default speed = 2 if not specified
                    width=entry.get("width", 200),  # Default width = 200 if not specified
                    height=entry.get("height", 40)  # Default height = 40 if not specified
                )

            self.platforms.add(platform)

    def check_platform_collision(self):
        # Check if the player is actually on a platform or something

        # Build a rect representing the player's position in WORLD coordinates
        player_rect = self.player.rect.copy()
        player_rect.centerx = int(self.player.world_x)     # World X center of the player
        player_rect.bottom = int(self.player.world_y)      # World Y feet of the player

        for platform in self.platforms:
            # Check if the player's feet are within the vertical landing zone of the platform
            if (player_rect.bottom >= platform.rect.top - 5 and
                    player_rect.bottom <= platform.rect.top + 15 and
                    player_rect.right > platform.rect.left + 5 and
                    player_rect.left < platform.rect.right - 5):

                # Only snap if the player is falling (jump_velocity > 0)
                if self.player.jump_velocity > 0:
                    self.player.world_y = platform.rect.top
                    self.player.jump_velocity = 0
                    self.player.on_ground = True

                    if isinstance(platform, MovingPlatform):
                        self.player.world_x += platform.delta_x  # Slide player horizontally with platform
                        self.player.world_y += platform.delta_y

                    return True

                return False

        return False




# ----------------------ENNEMIS STUFF--------------------------
    # ----------------------------------------------------- #
    #  ENNEMIS                                              #
    # ----------------------------------------------------- #

    def bird_spawn(self):
        bird = Bird(self, x=1400, y=200, velocity=4)
        self.flock.add(bird)




    def update_camera(self, screen_w, screen_h, world_w, world_h):
        # FROM AN OLD FILE
        """Update camera with deadzone scrolling"""
        SCROLL_MARGIN = 200

        player_screen_x = self.player.world_x - self.camera_x
        if player_screen_x > screen_w - SCROLL_MARGIN:
            self.camera_x = self.player.world_x - (screen_w - SCROLL_MARGIN)
        elif player_screen_x < SCROLL_MARGIN:
            self.camera_x = self.player.world_x - SCROLL_MARGIN

        player_screen_y = self.player.world_y - self.camera_y
        if player_screen_y > screen_h - SCROLL_MARGIN:
            self.camera_y = self.player.world_y - (screen_h - SCROLL_MARGIN)
        elif player_screen_y < SCROLL_MARGIN:
            self.camera_y = self.player.world_y - SCROLL_MARGIN

        self.camera_x = max(0, min(world_w - screen_w, self.camera_x))
        self.camera_y = max(0, min(world_h - screen_h, self.camera_y))

    def draw_world(self, screen, bg, cols, rows, cell_w, cell_h, screen_w, screen_h):
        # FROM AN OLD FILE
        """Draw the background grid"""
        for col in range(cols):
            for row in range(rows):
                screen_x = col * cell_w - self.camera_x
                screen_y = row * cell_h - self.camera_y
                if -cell_w < screen_x < screen_w and -cell_h < screen_y < screen_h:
                    screen.blit(bg[(col, row)], (screen_x, screen_y))

    def draw_objects(self, screen):
        # FROM AN OLD FILE
        """Draw all game objects"""
        # Draw bins
        for bin_obj in self.all_bins:
            screen_x = bin_obj.rect.x - self.camera_x
            screen_y = bin_obj.rect.y - self.camera_y
            screen.blit(bin_obj.image, (screen_x, screen_y))

        # Draw trash
        for trash in self.visible_trash:
            screen_x = trash.rect.x - self.camera_x
            screen_y = trash.rect.y - self.camera_y
            screen.blit(trash.image, (screen_x, screen_y))

        # Draw platforms
        for platform in self.platforms:
            screen_x = platform.rect.x - self.camera_x
            screen_y = platform.rect.y - self.camera_y
            screen.blit(platform.image, (screen_x, screen_y))

        # Sync and draw player
        self.player.rect.centerx = int(self.player.world_x - self.camera_x)
        self.player.rect.bottom = int(self.player.world_y - self.camera_y)
        screen.blit(self.player.image, self.player.rect)

    def draw_ui(self, screen):
        # FROM AN OLD FILE
        """Draw UI elements"""
        font = pygame.font.SysFont(None, 40)

        # Health bar
        screen.blit(self.player.health_image, (10, 50))
        self.player.update_health_bar()

        # Score and lives
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        lives_text = font.render(f"Vies: {self.lives}", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        # Carrying indicator
        if self.carrying:
            carry_text = font.render(f"Tu portes : {self.carried_trash_type}", True, (255, 255, 0))
            screen.blit(carry_text, (10, 90))