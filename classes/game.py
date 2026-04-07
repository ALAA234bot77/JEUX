

from classes.player import Player
from classes.trash import Trash
from classes.bin import Bin
from birdenemy import Bird
import pygame

#create a class to represent our game
class Game:

    def __init__(self):
        self.player = Player()
        self.pressed = {}
        self.score = 0
        self.lives = 3
        self.level = 1
        self.carrying = False
        self.carried_trash_type = None


        self.all_trash = self.create_trash()
        self.all_bins = self.create_bins()
        self.visible_trash = []

        self.flock = pygame.sprite.Group()
        self.bird_spawn()






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

    def throw_trash(self):
        if self.carrying:
            for bin in self.all_bins:
                bin_screen_rect = bin.rect.move(-self.camera_x, 0)
                if abs(self.player.rect.x - bin_screen_rect.x) < 100:
                    if self.carried_trash_type == bin.bin_type:
                        self.score += 1
                        print(f"✅ Bravo ! Score : {self.score}")
                    else:
                        self.lives -= 1
                        print(f"❌ Mauvaise poubelle ! Vies : {self.lives}")
                    self.carrying = False
                    self.carried_trash_type = None
                    return

    def bird_spawn(self):
        bird = Bird(x=1400, y=200, velocity=4)
        self.flock.add(bird)


def update_trash_visibility(self, camera_x, screen_w=1080):
    """
    Keep only trash that is close enough to appear on screen.
    camera_x comes from main, because main owns the camera.
    """
    self.visible_trash = []

    for trash in self.all_trash:
        screen_x = trash.rect.x - camera_x
        if -50 < screen_x < screen_w + 50:
            self.visible_trash.append(trash)

    def try_pickup_trash(self):
        """
        Pickup should be checked in world space.
        This assumes:
        - trash.rect.x / trash.rect.y are world positions
        - player.world_x / player.world_y are the real player positions
        """
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
        """
        Throwing must also be checked in world space.
        """
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