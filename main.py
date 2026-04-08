import pygame
from classes.game import Game
from main_menu import main_menu

pygame.init()
clock = pygame.time.Clock()

SCREEN_W, SCREEN_H = 1080, 720
pygame.display.set_caption("Trash Cat 67")
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# World settings -> to go 3 times up and down from a unique picture
COLS = 3
ROWS = 3
CELL_W = 1080
CELL_H = 720
WORLD_W = COLS * CELL_W
WORLD_H = ROWS * CELL_H

# Load background grid -> it will 'duplicate' the image 3 times right and 3 times up
bg = {}
for col in range(COLS):
    for row in range(ROWS):
        img = pygame.image.load(f'asset/bg_{col}_{row}.jpg')
        bg[(col, row)] = pygame.transform.scale(img, (CELL_W, CELL_H))


menu_choice = main_menu(screen)
# Start the game
if menu_choice == 'play':
    game = Game()
# Show credits screen TO DOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO !!!!!
#elif menu_choice == 'credits':
#    show_credits(screen)
# Quit the game
elif menu_choice == 'quit':
    pygame.quit()
    exit()

running = True
camera_x = 0
camera_y = 0

while running:



    # ---------- Health bar refresh -----------------
    screen.blit(game.player.health_image, (10, 50))
    game.player.update_health_bar()

    # -------- Event handling --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
            # Throw trash with E key
            if event.key == pygame.K_e:
                game.throw_trash()
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

    # -------- Player movement in world coordinates --------
    if game.pressed.get(pygame.K_d):
        game.player.move_right()
    if game.pressed.get(pygame.K_q):
        game.player.move_left()
    if game.pressed.get(pygame.K_SPACE):
        game.player.jump()

    # DO NOT CHANGE THE ORDER !
    # Reset on_ground at start of frame
    game.player.on_ground = False
    # Apply gravity
    game.player.apply_gravity(WORLD_H)
    # Check for platform collisions
    game.check_platform_collision()

    # N'ajoutez pas de double check is on ground.. j'ai perdu 2h de ma vie pur réussir à faire sauter le chat.. pas de double check...

    # -------- Clamp player to world edges --------
    game.player.world_x = max(75, min(WORLD_W - 75, game.player.world_x))
    game.player.world_y = max(0, min(WORLD_H - 30, game.player.world_y))

    # -------- Camera deadzone scrolling --------
    SCROLL_MARGIN = 200

    player_screen_x = game.player.world_x - camera_x
    if player_screen_x > SCREEN_W - SCROLL_MARGIN:
        camera_x = game.player.world_x - (SCREEN_W - SCROLL_MARGIN)
    elif player_screen_x < SCROLL_MARGIN:
        camera_x = game.player.world_x - SCROLL_MARGIN

    player_screen_y = game.player.world_y - camera_y
    if player_screen_y > SCREEN_H - SCROLL_MARGIN:
        camera_y = game.player.world_y - (SCREEN_H - SCROLL_MARGIN)
    elif player_screen_y < SCROLL_MARGIN:
        camera_y = game.player.world_y - SCROLL_MARGIN

    camera_x = max(0, min(WORLD_W - SCREEN_W, camera_x))
    camera_y = max(0, min(WORLD_H - SCREEN_H, camera_y))

    game.camera_x = camera_x
    game.camera_y = camera_y

    game.update_trash_visibility(SCREEN_W)
    game.try_pickup_trash()

    # -------- Draw world --------
    for col in range(COLS):
        for row in range(ROWS):
            screen_x = col * CELL_W - camera_x
            screen_y = row * CELL_H - camera_y
            if -CELL_W < screen_x < SCREEN_W and -CELL_H < screen_y < SCREEN_H:
                screen.blit(bg[(col, row)], (screen_x, screen_y))

    # -------- Draw bins --------
    for bin_obj in game.all_bins:
        screen_x = bin_obj.rect.x - camera_x
        screen_y = bin_obj.rect.y - camera_y
        screen.blit(bin_obj.image, (screen_x, screen_y))

    # -------- Draw trash --------
    for trash in game.visible_trash:
        screen_x = trash.rect.x - camera_x
        screen_y = trash.rect.y - camera_y
        screen.blit(trash.image, (screen_x, screen_y))

    # -------- Draw platforms ---------
    for platform in game.platforms:
        screen_x = platform.rect.x - camera_x
        screen_y = platform.rect.y - camera_y
        screen.blit(platform.image, (screen_x, screen_y))


    # -------- Sync and draw player --------
    game.player.rect.centerx = int(game.player.world_x - camera_x)
    game.player.rect.bottom = int(game.player.world_y - camera_y)
    screen.blit(game.player.image, game.player.rect)

    # -------- UI --------
    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
    lives_text = font.render(f"Vies: {game.lives}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))

    if game.carrying:
        carry_text = font.render(f"Tu portes : {game.carried_trash_type}", True, (255, 255, 0))
        screen.blit(carry_text, (10, 90))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()