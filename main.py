import pygame
import main_menu


def main_loop():
    pygame.init()
    pygame.display.set_caption("Trash Cat 67")
    # The display mode is set here so main_menu can use it.
    # main_menu will call pygame.display.set_mode again with the same size — that's fine.
    main_menu.main_menu()


main_loop()
