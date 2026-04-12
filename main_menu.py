import pygame
from buttons import Button
from Levels import Level_1



def get_font(size):
    return pygame.font.Font("asset/font.ttf", size)



def main_menu():
    pygame.init()
    pygame.mixer.music.load("asset/sound/main_menu_song.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode((1080, 720))
    background_raw = pygame.image.load("asset/bg_2_1.jpg")
    background = pygame.transform.scale(background_raw, (1080, 720))
    running = True
    while running:
        screen.blit(background, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(80).render("Trash Cat 67", True, "#11369E")
        menu_rect = menu_text.get_rect(center=(540, 100))

        play_button = Button(image=None, pos=(540, 250),text_input="PLAY", font=get_font(75), base_color="#d9fcd4", hovering_color="White")
        credits_button = Button(image=None, pos=(540, 400),text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        quit_button = Button(image=None, pos=(540, 550),text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        screen.blit(menu_text, menu_rect)

        for button in [play_button, credits_button, quit_button]:
            button.changeColor(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.checkForInput(menu_mouse_pos):
                    pygame.mixer.music.stop()
                    running = False
                    Level_1.level1(screen)
                    return
                if credits_button.checkForInput(menu_mouse_pos):
                    running = False
                    credits()
                    pygame.quit()
                    return
                if quit_button.checkForInput(menu_mouse_pos):
                    running = False
                    pygame.quit()
                    return

        def credits():
            SCREEN = pygame.display.set_mode((1080, 720))  # ← outside the loop
            while True:
                CREDITS_MOUSE_POS = pygame.mouse.get_pos()

                SCREEN.fill("white")

                CREDITS_TEXT = get_font(20).render("TO DO", True, "Black")
                CREDITS_RECT = CREDITS_TEXT.get_rect(center=(280, 100))
                SCREEN.blit(CREDITS_TEXT, CREDITS_RECT)

                CREDITS_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=get_font(75),
                                      base_color="Black", hovering_color="Green")

                CREDITS_BACK.changeColor(CREDITS_MOUSE_POS)
                CREDITS_BACK.update(SCREEN)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                            main_menu()

                pygame.display.update()

        pygame.display.update()

