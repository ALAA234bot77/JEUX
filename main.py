import pygame
from classes.game import Game

"""This is the main program"""
pygame.init()

clock = pygame.time.Clock()
clock.tick(60)

# fonction spawn oiseau (instable)
"""game.flock.draw(screen)
    for bird in game.flock:
        if bird.rect.x < 700:
            bird.forward()
        elif bird.rect.x > 700:
            while bird.rect.x > 0:
                bird.backward()"""

#generer notre ecran
pygame.display.set_caption("Trash Cat 67")
screen = pygame.display.set_mode((1080,720))
background_img=pygame.image.load('asset/bg_brouillon.jpg')
back
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            if event.key == ord('f'):
                game.throw_trash()

        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

    clock.tick(60)
