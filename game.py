from classes.player import Player
from classes.trash import Trash
from classes.bin import Bin

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
                    self.carried_trash_type = trash.trash_type

    def create_trash(self):
        if self.level == 1:
            return [
                Trash(800, "recyclable"),
                Tras
