
from player import Player
from trash import Trash

#create a class to represent our game
class Game:

    def __init__(self):
        self.player = Player()
        self.pressed={}
        self.score=0
         self.all_trash = [
            Trash(800),
            Trash(1200),
            Trash(1600),
            Trash(2000),
        ]
        self.visible_trash = []
        self.camera_x = 0

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
                self.all_trash.remove(trash)
                if trash in self.visible_trash:
                    self.visible_trash.remove(trash)
                self.score += 1
