import pygame
from game import Game
"""This is the main program"""
pygame.init()

clock = pygame.time.Clock()
clock.tick(60)


#generer notre ecran
pygame.display.set_caption("Trash Cat 67")
screen = pygame.display.set_mode((1080,720))
background_img=pygame.image.load('asset/bg_brouillon.jpg')
background= pygame.transform.scale(background_img,(1080,720)) #change the size of the background to size of screen

# import the background

#charger le jeux
game = Game()
running = True


while running:

    #appliquer la fenetre de jeu
    screen.blit(background,(0,0))

    #appliquer l'image du joueur
    screen.blit(game.player.image, game.player.rect)

    #verifier si on va gauche ou droite:
    if game.pressed.get(pygame.K_RIGHT) and game.player.rect.x < 950:
        game.player.move_right()
    if game.pressed.get(pygame.K_LEFT) and game.player.rect.x > 0:
        game.player.move_left()

    if game.pressed.get(pygame.K_SPACE):
        game.player.jump()

    game.player.apply_gravity()
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

    clock.tick(60)