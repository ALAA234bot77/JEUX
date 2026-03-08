import pygame
"""This is the main program"""
pygame.init()

#create a class to represent our game
class Game:

    def __init__(self):
        self.player = Player()


# create a class to represent the player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.max_health = 3
        self.image = pygame.image.load('asset/perso_67.webp')
        self.rect = self.image.get_rect()
        self.rect.x = 300
        self.rect.y =300


pygame.display.set_caption("Trash Cat 67")
screen = pygame.display.set_mode((1080,720))

# import the background
background=pygame.image.load('asset/bg_brouillon.jpg')

game = Game()
running = True

while running:

    #appliquer la fenetre de jeu
    screen.blit(background,(200,200))

    #appliquer l'image du joueur
    screen.blit(game.player.image, game.player.rect)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()