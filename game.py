"""from classes.player import Player
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
        self.camera_x = 0

        self.all_trash = self.create_trash()
        self.all_bins = self.create_bins()
        self.visible_trash = []



        self.flock = pygame.sprite.Group()
        self.bird_spawn()

    def bird_spawn(self):
        bird = Bird()
        self.flock.add(bird)

    def update_camera(self):
        self.camera_x = self.player.rect.x - 400

    def update_trash_visibility(self):
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
                    self.carried_trash_type = trash.trash_type"""

