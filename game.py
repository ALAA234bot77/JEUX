
from player import Player
from birdenemy import Bird

#create a class to represent our game
class Game:

    def __init__(self):
        self.player = Player()
        self.pressed={}

    #def bird_spawn(self):
     #   bird = Bird()