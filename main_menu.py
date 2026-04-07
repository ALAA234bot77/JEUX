import pygame
from buttons import Button
#from main import screen, background_img

pygame.init()
def get_font(size):
    return pygame.font.Font("asset/font.ttf", size)

screen = pygame.display.set_mode((1080,720))

background = pygame.image.load("asset/bg_brouillon.jpg")

def main_menu():
    running = True
    while running:
        screen.blit(background, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("Trash Cat 67", True, "#11369E")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=None, pos=(640, 250),text_input="PLAY", font=get_font(75), base_color="#d9fcd4", hovering_color="White")
        CREDITS_BUTTON = Button(image=None, pos=(640, 400),text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 550),text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, CREDITS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    #play()
                    pygame.quit()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    #credits()
                    pygame.quit()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    running = False
                    pygame.quit()


        pygame.display.update()


main_menu()