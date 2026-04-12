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

                CREDITS_TITLE = get_font(50).render("Credits", True, "Black")
                CREDITS_TITLE_RECT = CREDITS_TITLE.get_rect(center=(540, 50))
                SCREEN.blit(CREDITS_TITLE, CREDITS_TITLE_RECT)

                CREATORS_TITLE = get_font(30).render("Creators", True, "Blue")
                CREATORS_TITLE_RECT = CREATORS_TITLE.get_rect(center=(540, 120))
                SCREEN.blit(CREATORS_TITLE, CREATORS_TITLE_RECT)

                CREATORS_SUB = get_font(20).render("This game was designed and built by:", True, "Black")
                CREATORS_SUB_RECT = CREATORS_SUB.get_rect(center=(540, 155))
                SCREEN.blit(CREATORS_SUB, CREATORS_SUB_RECT)

                CREATORS_NAMES = get_font(20).render("Pauline  Emeline  Kavani  Alaa  Yann  Leonard  Fatoumata", True, "Black")
                CREATORS_NAMES_RECT = CREATORS_NAMES.get_rect(center=(540, 183))
                SCREEN.blit(CREATORS_NAMES, CREATORS_NAMES_RECT)

                THANKS_TITLE = get_font(30).render("Special Thanks", True, "Blue")
                THANKS_TITLE_RECT = THANKS_TITLE.get_rect(center=(540, 230))
                SCREEN.blit(THANKS_TITLE, THANKS_TITLE_RECT)

                THANKS_1 = get_font(20).render("A big thanks to all little guys who answered :", True, "Black")
                THANKS_1_RECT = THANKS_1.get_rect(center=(540, 265))
                SCREEN.blit(THANKS_1, THANKS_1_RECT)

                THANKS_2 = get_font(20).render("'what kind of game you want to play ?'", True, "Black")
                THANKS_2_RECT = THANKS_2.get_rect(center=(540, 290))
                SCREEN.blit(THANKS_2, THANKS_2_RECT)

                THANKS_3 = get_font(20).render("they all said the same thing:", True, "Black")
                THANKS_3_RECT = THANKS_3.get_rect(center=(540, 315))
                SCREEN.blit(THANKS_3, THANKS_3_RECT)

                THANKS_4 = get_font(20).render("A game with brainrot.", True, "Red")
                THANKS_4_RECT = THANKS_4.get_rect(center=(540, 340))
                SCREEN.blit(THANKS_4, THANKS_4_RECT)

                THANKS_5 = get_font(20).render("Challenge accepted. We hope we delivered.", True, "Black")
                THANKS_5_RECT = THANKS_5.get_rect(center=(540, 365))
                SCREEN.blit(THANKS_5, THANKS_5_RECT)

                EFREI_TITLE = get_font(30).render("EFREI", True, "Blue")
                EFREI_TITLE_RECT = EFREI_TITLE.get_rect(center=(540, 410))
                SCREEN.blit(EFREI_TITLE, EFREI_TITLE_RECT)

                EFREI_1 = get_font(20).render("We would like to express our gratitude to EFREI", True, "Black")
                EFREI_1_RECT = EFREI_1.get_rect(center=(540, 443))
                SCREEN.blit(EFREI_1, EFREI_1_RECT)

                EFREI_2 = get_font(20).render("for providing us with the tools, resources, and support", True, "Black")
                EFREI_2_RECT = EFREI_2.get_rect(center=(540, 468))
                SCREEN.blit(EFREI_2, EFREI_2_RECT)

                EFREI_3 = get_font(20).render("that made this project possible.", True, "Black")
                EFREI_3_RECT = EFREI_3.get_rect(center=(540, 493))
                SCREEN.blit(EFREI_3, EFREI_3_RECT)

                CREDITS_BACK = Button(image=None, pos=(640, 460), text_input="BACK", font=get_font(75),
                                      base_color="Black", hovering_color="Green")

                COPYRIGHT_TITLE = get_font(30).render("Copyright", True, "Blue")
                COPYRIGHT_TITLE_RECT = COPYRIGHT_TITLE.get_rect(center=(540, 538))
                SCREEN.blit(COPYRIGHT_TITLE, COPYRIGHT_TITLE_RECT)

                COPYRIGHT_1 = get_font(20).render("Toby Fox for the song 'School'", True, "Black")
                COPYRIGHT_1_RECT = COPYRIGHT_1.get_rect(center=(540, 571))
                SCREEN.blit(COPYRIGHT_1, COPYRIGHT_1_RECT)

                COPYRIGHT_2 = get_font(20).render("8-bit universe for the song 'Take On Me'",True, "Black")
                COPYRIGHT_2_RECT = COPYRIGHT_2.get_rect(center=(540, 596))
                SCREEN.blit(COPYRIGHT_2, COPYRIGHT_2_RECT)

                COPYRIGHT_3 = get_font(20).render("Pac-man for SFX", True, "Black")
                COPYRIGHT_3_RECT = COPYRIGHT_3.get_rect(center=(540, 621))
                SCREEN.blit(COPYRIGHT_3, COPYRIGHT_3_RECT)

                CREDITS_BACK = Button(image=None, pos=(540, 670), text_input="BACK", font=get_font(40),
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

