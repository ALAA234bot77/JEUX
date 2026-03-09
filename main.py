import pygame
from game import Game
"""This is the main program"""
pygame.init()




#generer notre ecran
pygame.display.set_caption("Trash Cat 67")
screen = pygame.display.set_mode((1080,720))

# import the background
background=pygame.image.load('asset/bg_brouillon.jpg')
#charger le jeux
game = Game()
running = True

while running:

    #appliquer la fenetre de jeu
    screen.blit(background,(200,200))

    #appliquer l'image du joueur
    screen.blit(game.player.image, game.player.rect)

    #verifier si on va gauche ou droite:
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x < 870:
        game.player.move_right()
    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 192:
        game.player.move_left()
    print(game.player.rect.x,game.player.rect.y)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        #decter si le jouer lache une touch
        elif event.type == pygame.KEYDOWN:#quel touche etait appuile
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False


