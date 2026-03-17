
from player import Player
from trash import Trash
from bin import Bin

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
