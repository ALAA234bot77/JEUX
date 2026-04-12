from classes.platform import Platform, MovingPlatform
from classes.player import Player
from classes.spike import spike
from classes.trash import Trash
from classes.bin import Bin
from classes.birdenemy import Bird
import pygame
import math

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
        self.lives = 3 # plus utile mais je garde au cas ou quelqu'un veille re utiliser des truc que j'ai passer en commentaire
        self.level = 1
        self.goal = 0
        self.carrying = False
        self.carried_trash_type = None
        self.carried_trash_image = None

        self.camera_x = 0
        self.camera_y = 0

        self.all_trash = self.create_trash()
        self.all_bins = self.create_bins()
        self.all_spike = self.create_spike()
        self.visible_trash = []

        self.flock = pygame.sprite.Group()
        #self.bird_spawn()

        self.immunity = False

        self.platforms = pygame.sprite.Group()
        self.platform_spawn()

        # Throw / arc system
        self.throw_state = "idle"
        self.drag_start = None  # screen (x, y) where drag began

        self.proj_world_x = 0.0
        self.proj_world_y = 0.0
        self.proj_vx = 0.0
        self.proj_vy = 0.0

        self.PROJ_GRAVITY = 0.4  # px / frame²
        self.POWER_SCALE = 0.18  # drag px → px/frame
        self.MAX_DRAG = 220  # max drag distance in screen px

        self.FLOAT_OFFSET_Y = -90  # px above player.world_y where trash floats

    def check_collisions(self, sprite, group):
        return pygame.sprite.spritecollide(sprite, group, False, pygame.sprite.collide_mask)


# ─────────────────────── BACKGROUND ───────────────────────────────────────────

    def load_background(self,bg,cols,rows,cell_w,cell_h):
        for col in range(cols):
            for row in range(rows):
                img = pygame.image.load(f'asset/bg_{col}_{row}.jpg')
                bg[(row,col)] = pygame.transform.scale(img, (cell_w, cell_h))

    def draw_background(self, screen,bg,cols,rows,cell_w,cell_h,screen_w, screen_h):
        for col in range(cols):
            for row in range(rows):
                screen_x = col*cell_w -self.camera_x
                screen_y = row*cell_h -self.camera_y
                if -cell_w < screen_x < screen_w and -cell_h < screen_y < screen_h:
                    screen.blit(bg[(row,col)], (screen_x, screen_y))

# ─────────────────────── CAMERA ───────────────────────────────────────────────
    def update_camera(self, screen_w,screen_h, world_w, world_h):
        SCROLL_MARGIN = 200

        player_screen_x = self.player.world_x - self.camera_x
        if player_screen_x > screen_w-SCROLL_MARGIN:
            self.camera_x = self.player.world_x- (screen_w-SCROLL_MARGIN)
        elif player_screen_x < SCROLL_MARGIN:
            self.camera_x = self.player.world_x -SCROLL_MARGIN

        player_screen_y = self.player.world_y - self.camera_y
        if player_screen_y > screen_h-SCROLL_MARGIN:
            self.camera_y = self.player.world_y - (screen_h-SCROLL_MARGIN)
        elif player_screen_y < SCROLL_MARGIN:
            self.camera_y = self.player.world_y -SCROLL_MARGIN

        self.camera_x = max(0, min(world_w - screen_w, self.camera_x))
        self.camera_y = max(0, min(world_h - screen_h, self.camera_y))

# ─────────────────────── DRAWING ──────────────────────────────────────────────
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
            if isinstance(platform, MovingPlatform): #to update them before drawing them
                platform.update()
            screen_x = platform.rect.x - self.camera_x
            screen_y = platform.rect.y - self.camera_y
            screen.blit(platform.image, (screen_x, screen_y))

        # Draw the spikes
        for spike in self.all_spike:
            screen_x = spike.rect.x - self.camera_x
            screen_y = spike.rect.y - self.camera_y
            screen.blit(spike.image, (screen_x, screen_y))

        # Sync and draw player
        self.player.rect.centerx = int(self.player.world_x - self.camera_x)
        self.player.rect.bottom = int(self.player.world_y - self.camera_y)
        screen.blit(self.player.image, self.player.rect)

        # Draw carried trash + arc preview
        self.draw_carried_trash(screen)
        mouse_pos = pygame.mouse.get_pos()
        if self.throw_state == "dragging" and self.carrying:
            self._draw_arc_preview(screen, mouse_pos)
            self._draw_bin_highlight(screen, mouse_pos)


    def draw_ui(self,screen,lose=False):
        font = pygame.font.SysFont("Arial", 20)

        self.player.update_health_bar()
        screen.blit(pygame.transform.scale(self.player.health_image, (120, 50)), (10, 50))

        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        if self.carrying:
            carry_text = font.render(f"Tu portes : {self.carried_trash_type}", True, (255, 255, 0))
            screen.blit(carry_text, (10, 90))






        #arc throw moved from main
    def _draw_arc_preview(self, screen, mouse_pos):
        points = self.get_trajectory_points(mouse_pos)
        for i, pt in enumerate(points):
            if i % 3 == 0:
                pygame.draw.circle(screen, (255, 255, 255), pt, 3)
        hx, hy = self._hold_pos()
        hold_sx = int(hx - self.camera_x)
        hold_sy = int(hy - self.camera_y)
        pygame.draw.line(screen, (200, 100, 100), (hold_sx, hold_sy), mouse_pos, 2)


    def _draw_bin_highlight(self, screen, mouse_pos):
        # FIX: Same as above — moved here from Level_1.py.
        aimed = self.get_aimed_bin(mouse_pos)
        if aimed is None:
            return
        correct = (aimed.bin_type == self.carried_trash_type)
        colour = (80, 255, 80) if correct else (255, 80, 80)
        sx = int(aimed.rect.x - self.camera_x) - 5
        sy = int(aimed.rect.y - self.camera_y) - 5
        w = aimed.rect.width + 10
        h = aimed.rect.height + 10
        pygame.draw.rect(screen, colour, (sx, sy, w, h), 4, border_radius=6)
        font_s = pygame.font.SysFont(None, 28)
        label = font_s.render(aimed.bin_type, True, colour)
        screen.blit(label, (sx + w // 2 - label.get_width() // 2, sy - 22))

# ─────────────────────── THROW / ARC SYSTEM ───────────────────────────────────


    def _hold_pos(self):
        """World position of the floating trash (above player head)."""  # ← NEW
        return (self.player.world_x, self.player.world_y + self.FLOAT_OFFSET_Y)

    def _drag_velocity(self, drag_start, mouse_pos):  # ← NEW
        """Pull-back gesture → forward velocity (px/frame)."""
        dx = drag_start[0] - mouse_pos[0]
        dy = drag_start[1] - mouse_pos[1]
        length = math.hypot(dx, dy)
        if length > self.MAX_DRAG:
            dx = dx / length * self.MAX_DRAG
            dy = dy / length * self.MAX_DRAG
        return dx * self.POWER_SCALE, dy * self.POWER_SCALE

    def start_drag(self, mouse_pos):  # ← NEW
        if self.carrying and self.throw_state == "idle":
            self.throw_state = "dragging"
            self.drag_start = mouse_pos

    def release_drag(self, mouse_pos):  # ← NEW
        if self.throw_state != "dragging" or self.drag_start is None:
            return
        vx, vy = self._drag_velocity(self.drag_start, mouse_pos)
        if math.hypot(vx, vy) < 0.5:
            self.throw_state = "idle"
            return
        hx, hy = self._hold_pos()
        self.proj_world_x = float(hx)
        self.proj_world_y = float(hy)
        self.proj_vx = vx
        self.proj_vy = vy
        self.throw_state = "flying"

    def update_projectile(self):  # ← NEW: replaces the old throw_trash(). No dt parameter.
        """Advance projectile one frame. Call once per frame (no dt)."""
        if self.throw_state != "flying":
            return

        self.proj_vy += self.PROJ_GRAVITY
        self.proj_world_x += self.proj_vx
        self.proj_world_y += self.proj_vy

        def platform_spawn(self):
            self.platforms.empty()  # On vide pour éviter les doublons
            o = (self.level - 1) * 1080
            positions = self.PLATFORMS_BY_LEVEL.get(self.level, [])

            for entry in positions:
                if isinstance(entry, tuple):
                    x_relative, y = entry
                    # On ajoute l'offset 'o' pour placer la plateforme dans le bon niveau
                    platform = Platform(self, x=o + x_relative, y=y)
                elif isinstance(entry, dict):
                    platform = MovingPlatform(
                        self,
                        x=o + entry["x"],
                        y=entry["y"],
                        target_x=o + entry["target_x"],  # Ajout de o ici aussi !
                        target_y=entry["target_y"],  # On ne touche pas au Y global
                        speed=entry.get("speed", 2)
                    )
                self.platforms.add(platform)

        # Bin collision
        for bin_obj in self.all_bins:
            if (abs(self.proj_world_x - bin_obj.rect.centerx) < 45 and
                    abs(self.proj_world_y - bin_obj.rect.centery) < 60):
                if self.carried_trash_type == bin_obj.bin_type:
                    self.score += 1
                    self.goal -= 1
                    print(f"✅ Bravo ! Score : {self.score}")
                else:
                    self.goal -= 1
                    self.player.health -= 1
                    self.player.update_health_bar()
                    print(f"❌ Mauvaise poubelle !")
                self.carrying = False
                self.carried_trash_type = None
                self.carried_trash_image = None
                self.throw_state = "idle"
                return

        # ← NEW: missed → return to hand instead of disappearing
        floor_y = 3 * 720 - 30
        if (self.proj_world_y > floor_y or
                self.proj_world_x < 0 or
                self.proj_world_x > 3 * 1080):
            print("💨 Raté — retour en main")
            self.throw_state = "idle"  # trash stays in hand, player can aim again

    def get_trajectory_points(self, mouse_pos, steps=55):  # ← NEW
        """
        Screen-space arc preview dots.
        Uses the EXACT same physics as update_projectile — preview matches reality.
        """
        if self.drag_start is None:
            return []
        vx, vy = self._drag_velocity(self.drag_start, mouse_pos)
        if math.hypot(vx, vy) < 0.5:
            return []
        hx, hy = self._hold_pos()
        px, py = float(hx), float(hy)
        pvx, pvy = vx, vy
        points = []
        for _ in range(steps):
            sx = int(px - self.camera_x)
            sy = int(py - self.camera_y)
            points.append((sx, sy))
            pvy += self.PROJ_GRAVITY
            px += pvx
            py += pvy
            if py > 3 * 720:
                break
        return points

    def get_aimed_bin(self, mouse_pos):  # ← NEW
        """Return the first bin the simulated arc hits, or None."""
        if self.drag_start is None:
            return None
        vx, vy = self._drag_velocity(self.drag_start, mouse_pos)
        if math.hypot(vx, vy) < 0.5:
            return None
        hx, hy = self._hold_pos()
        px, py = float(hx), float(hy)
        pvx, pvy = vx, vy
        for _ in range(80):
            pvy += self.PROJ_GRAVITY
            px += pvx
            py += pvy
            for bin_obj in self.all_bins:
                if (abs(px - bin_obj.rect.centerx) < 50 and
                        abs(py - bin_obj.rect.centery) < 65):
                    return bin_obj
        return None

    def draw_carried_trash(self, screen):  # ← NEW: replaces the old circle draw
        """
        Draw the actual trash sprite:
          - floating above player when idle/dragging
          - at projectile position when flying
        """
        if not self.carrying or self.carried_trash_image is None:
            return
        img = self.carried_trash_image

        if self.throw_state in ("idle", "dragging"):
            hx, hy = self._hold_pos()
            sx = int(hx - self.camera_x) - img.get_width() // 2
            sy = int(hy - self.camera_y) - img.get_height() // 2
        else:  # flying
            sx = int(self.proj_world_x - self.camera_x) - img.get_width() // 2
            sy = int(self.proj_world_y - self.camera_y) - img.get_height() // 2

        screen.blit(img, (sx, sy))


# ─────────────────────── TRASH ────────────────────────────────────────────────
    # generate all the trash for a lvl, add some trash to the list if you want more trash
    def create_trash(self):
        o = (self.level - 1) * 1080  # origin : 0, 1080 ou 2160
        if self.level == 1:
            self.goal = 4
            return [
                Trash(o + 300, 2125, "recyclable"),
                Trash(o + 500, 2125, "menager"),
                Trash(o + 600, 2125, "recyclable"),
                Trash(o + 900, 2125, "menager"),
            ]
        elif self.level == 2:
            self.goal = 4
            return [
                Trash(o + 300, 2125, "recyclable"),
                Trash(o + 500, 2125, "menager"),
                Trash(o + 700, 2125, "compost"),
                Trash(o + 900, 2125, "papier"),
            ]
        elif self.level == 3:
            self.goal = 6
            return [
                Trash(o + 200, 2125, "recyclable"),
                Trash(o + 380, 2125, "menager"),
                Trash(o + 520, 2125, "compost"),
                Trash(o + 660, 2125, "papier"),
                Trash(o + 800, 2125, "verre"),
                Trash(o + 940, 2125, "vetement"),
            ]

    def create_bins(self):
        o = (self.level - 1) * 1080
        if self.level == 1:
            return [
                Bin(o + 100, 2125, "recyclable"),
                Bin(o + 180, 2125, "menager"),
            ]
        elif self.level == 2:
            return [
                Bin(o + 80, 2125, "recyclable"),
                Bin(o + 160, 2125, "menager"),
                Bin(o + 240, 2125, "compost"),
                Bin(o + 320, 2125, "papier"),
            ]
        elif self.level == 3:
            return [
                Bin(o + 60, 2125, "recyclable"),
                Bin(o + 130, 2125, "menager"),
                Bin(o + 200, 2125, "compost"),
                Bin(o + 270, 2125, "papier"),
                Bin(o + 340, 2125, "verre"),
                Bin(o + 410, 2125, "vetement"),
            ]


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
                self.carried_trash_image = trash.image  #  save image for floating draw
                self.throw_state = "idle"  #  reset throw state on pickup
                return

    def throw_trash_instant(self):
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
                    self.goal -= 1
                    print(self.goal)
                    print(f"✅ Bravo ! Score : {self.score}")
                else:
                    self.goal -= 1
                    print(self.goal)
                    self.player.health -= 1
                    self.player.update_health_bar()
                    print(f"❌ Mauvaise poubelle ! Vies : {self.player.health}")

                self.carrying = False
                self.carried_trash_type = None
                return

    def next_lvl(self):
        self.level += 1
        if self.level > 3:
            self.level = 3
            return 'victory'
        self.all_trash = self.create_trash()
        self.all_bins = self.create_bins()
        self.all_spike = self.create_spike()
        self.platforms.empty()
        self.platform_spawn()
        self.player.health = 3
        self.player.update_health_bar()
        self.carrying = False
        self.carried_trash_type = None
        self.carried_trash_image = None
        self.throw_state = "idle"
        return None





# ─────────────────────── PLATFORMS ────────────────────────────────────────────


    # If you want to add a STATIC platform, simply put his coordinates in a tuple right here. You don't have to modify anything else.
    # If you want to add a MOVING platform, put in a dictionary from which coordinated to which you want it to move

    PLATFORMS_BY_LEVEL = {
        1: [
            (50, 250),
            (300, 1980),
            (600, 1920),
            {"x": 600, "y": 1780, "target_x": 750, "target_y": 1780, "speed": 2},
        ],
        2: [
            (800, 1260),
            (450, 1230),
            (200, 1130),
            {"x": 600, "y": 980, "target_x": 1100, "target_y": 980, "speed": 2},
        ],
        3: [
            (800, 540),
            (450, 510),
            (200, 410),
            {"x": 600, "y": 260, "target_x": 1100, "target_y": 260, "speed": 3},
        ],
    }

    def platform_spawn(self):
        self.platforms.empty() # On vide pour éviter les doublons
        o = (self.level - 1) * 1080
        positions = self.PLATFORMS_BY_LEVEL.get(self.level, [])

        for entry in positions:
            if isinstance(entry, tuple):
                x_relative, y = entry
                # On ajoute l'offset 'o' pour placer la plateforme dans le bon niveau
                platform = Platform(self, x=o + x_relative, y=y)
            elif isinstance(entry, dict):
                platform = MovingPlatform(
                    self,
                    x= o + entry["x"],
                    y=entry["y"],
                    target_x= o + entry["target_x"], # Ajout de o ici aussi !
                    target_y=entry["target_y"],      # On ne touche pas au Y global
                    speed=entry.get("speed", 2)
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




# ─────────────────────── ENEMIES ──────────────────────────────────────────────

    def bird_spawn(self):
        bird = Bird(self, x=1400, y=200, velocity=4)
        self.flock.add(bird)

    def damage(self):
        for spike in self.all_spike:
            if (abs(self.player.world_x - spike.rect.x) < 50)and(abs(self.player.world_y - spike.rect.bottom) < 50):
                if not spike.immunity:
                    self.player.health -= 1
                    self.player.update_health_bar()
                    spike.immunity = True
            if (abs(self.player.world_x - spike.rect.x) > 70)or((self.player.world_y - spike.rect.bottom) > 70):
                spike.immunity = False

    def create_spike(self):
        o = (self.level - 1) * 1080
        if self.level == 1:
            return [spike(o + 400, 2125), spike(o + 700, 2125)]
        elif self.level == 2:
            return [spike(o + 300, 2125), spike(o + 450, 2125),
                    spike(o + 600, 2125), spike(o + 750, 2125)]
        elif self.level == 3:
            return [spike(o + 250, 2125), spike(o + 380, 2125),
                    spike(o + 510, 2125), spike(o + 640, 2125),
                    spike(o + 770, 2125), spike(o + 900, 2125)]

