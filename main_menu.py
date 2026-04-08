import pygame
from buttons import Button

pygame.init()

# Get pretty font with a good size easily
def get_font(size):
    return pygame.font.Font("asset/font.ttf", size)

background = pygame.image.load("asset/menu_bg.png")

# Displays the main menu and handles user input. Returns a string 'play', 'credits' or 'quit'.
def main_menu(screen):
    running = True
    while running:
        # Draw the background
        screen.blit(background, (0, 0))

        # For button hover effects
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(80).render("Trash Cat 67", True, "#11369E")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        # Create the 3 buttons
        PLAY_BUTTON = Button(image=None, pos=(640, 250),text_input="PLAY", font=get_font(75), base_color="#d9fcd4", hovering_color="White")
        CREDITS_BUTTON = Button(image=None, pos=(640, 400),text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=None, pos=(640, 550),text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        # Draw the title and buttons on the screen
        screen.blit(MENU_TEXT, MENU_RECT)
        for button in [PLAY_BUTTON, CREDITS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        # Handle events (mouse clicks, window close, etc.)
        for event in pygame.event.get():

            # User closed the window
            if event.type == pygame.QUIT:
                return 'quit'

            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'play'
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'credits'
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    return 'quit'

        # Update the display
        pygame.display.update()

    # This line is a fallback, but the loop will always return before reaching here
    return 'quit'