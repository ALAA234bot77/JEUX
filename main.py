import pygame


pygame.init()
"""This is the main program"""
pygame.display.set_caption("game")
pygame.display.set_mode((1080,720))

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()