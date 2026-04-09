import pygame
from classes.game import Game
import main_menu
from classes.platform import Platform, MovingPlatform
from buttons import Button

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


# Start the game
menu_choice = main_menu.main_menu(screen)

# credit managment
while menu_choice == "credits":
    credits_choice = main_menu.credits(screen)

    if credits_choice == "back":
        menu_choice = main_menu.main_menu(screen)

    elif credits_choice == "quit":
        pygame.quit()
        exit()

# start the game
if menu_choice == "play":
    game = Game()

# leave
elif menu_choice == "quit":
    pygame.quit()
    exit()

running = True
camera_x = 0
camera_y = 0
lose = False

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
    if not lose : # when game over you can move but the game don't close instantly
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

    # -------- Draw & update platforms ---------
    for platform in game.platforms:
        # Update position if it's a moving platform
        if isinstance(platform, MovingPlatform):
            platform.update()

        # Draw every platform (static and moving) at its current position
        screen_x = platform.rect.x - camera_x  # Convert world X to screen X
        screen_y = platform.rect.y - camera_y  # Convert world Y to screen Y
        screen.blit(platform.image, (screen_x, screen_y))

    # -------- draw spike -----------
    for spike in game.all_spike:
        screen_x = spike.rect.x - camera_x  # Convert world X to screen X
        screen_y = spike.rect.y - camera_y  # Convert world Y to screen Y
        screen.blit(spike.image, (screen_x, screen_y))
        game.damage()


    # -------- Sync and draw player --------
    game.player.rect.centerx = int(game.player.world_x - camera_x)
    game.player.rect.bottom = int(game.player.world_y - camera_y)
    screen.blit(game.player.image, game.player.rect)

    # -------- UI --------
    font = pygame.font.SysFont(None, 40)

    game.player.update_health_bar()
    screen.blit(pygame.transform.scale(game.player.health_image,(120,50)), (10, 50))

    score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
    #lives_text = font.render(f"Vies: {game.lives}", True, (255, 0, 0))
    screen.blit(score_text, (10, 10))
    #screen.blit(lives_text, (10, 50))

    if game.carrying:
        carry_text = font.render(f"Tu portes : {game.carried_trash_type}", True, (255, 255, 0))
        screen.blit(carry_text, (10, 90))

    if game.lives == 0:
        end_text = font.render("Game Over", True, (255, 0, 0))
        screen.blit(end_text, (450, 350))
        lose = True

    # --------- refresh of lvl ----------------
    if (game.next_lvl() == "victory"):
        font = pygame.font.SysFont(None, 80)
        win_text = font.render("Victory", True, (0, 0, 255))
        screen.blit(win_text, (450, 350))
        lose = True


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
