import pygame
from classes.game import Game
from classes.timer import Timer
from classes.platform import Platform, MovingPlatform

"""
# ── Draw  for arc throw
def draw_arc_preview(screen, game, mouse_pos):  # ← NEW

    points = game.get_trajectory_points(mouse_pos)
    for i, pt in enumerate(points):
        if i % 3 == 0:
            pygame.draw.circle(screen, (255, 255, 255), pt, 3)
    hx, hy = game._hold_pos()
    hold_sx = int(hx - game.camera_x)
    hold_sy = int(hy - game.camera_y)
    pygame.draw.line(screen, (200, 100, 100), (hold_sx, hold_sy), mouse_pos, 2)


def draw_bin_highlight(screen, game, mouse_pos):  # ← NEW
    
    aimed = game.get_aimed_bin(mouse_pos)
    if aimed is None:
        return
    correct = (aimed.bin_type == game.carried_trash_type)
    colour = (80, 255, 80) if correct else (255, 80, 80)
    sx = int(aimed.rect.x - game.camera_x) - 5
    sy = int(aimed.rect.y - game.camera_y) - 5
    w = aimed.rect.width + 10
    h = aimed.rect.height + 10
    pygame.draw.rect(screen, colour, (sx, sy, w, h), 4, border_radius=6)
    font_s = pygame.font.SysFont(None, 28)
    label = font_s.render(aimed.bin_type, True, colour)
    screen.blit(label, (sx + w // 2 - label.get_width() // 2, sy - 22))
"""





def level1(screen):
    clock = pygame.time.Clock()
    timer = Timer(300)
    SCREEN_W, SCREEN_H = 1080, 720
    pygame.display.set_caption("Trash Cat 67")

    game = Game()

    COLS = 3
    ROWS = 3
    CELL_W = 1080
    CELL_H = 720
    WORLD_W = COLS * CELL_W
    WORLD_H = ROWS * CELL_H
    # Load background grid -> it will 'duplicate' the image 3 times right and 3 times up
    bg = {}
    game.load_background(bg, COLS, ROWS, CELL_W, CELL_H)

    running = True
    # camera_x = 0
    # camera_y = 0
    lose = False
    #transition entre levels
    transitioning = False
    fading_in = False
    fading_out = False
    fade = 0
    fade_surface = pygame.Surface((SCREEN_W, SCREEN_H))
    fade_surface.fill((0, 0, 0))

    while True:
        # -------- Events --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            elif event.type == pygame.KEYDOWN:
                game.pressed[event.key] = True
                if event.key == pygame.K_e:
                    game.throw_trash_instant()
                if event.key == pygame.K_p:
                    timer.set_pause()
                    if timer.paused:
                        game.pressed = {}
                #restart
                if event.key == pygame.K_r and timer.finished:
                    timer.restart()
                    game.__init__()
                    lose = False
                    transitioning = False
                    fading_in = False
                    fading_out = False
                    fade = 0

            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.start_drag(event.pos)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game.release_drag(event.pos)

        # -------- Player movement in world coordinates --------
        if not lose and not timer.paused and not timer.finished and not transitioning:
            if game.pressed.get(pygame.K_d):
                game.player.move_right()
            if game.pressed.get(pygame.K_q):
                game.player.move_left()
            if game.pressed.get(pygame.K_SPACE):
                game.player.jump()

        # -------- Physics (DO NOT CHANGE THE ORDER) --------
        # Reset on_ground at start of frame
        game.player.on_ground = False
        # Apply gravity
        game.player.apply_gravity(WORLD_H)
        # Check for platform collisions
        game.check_platform_collision()

        # N'ajoutez pas de double check is on ground.. j'ai perdu 2h de ma vie pur réussir à faire sauter le chat.. pas de double check...

        game.update_projectile()  # advance projectile physics every frame

        # -------- Clamp player to world edges --------
        # Bloque le joueur dans la colonne de son niveau tant que goal n'est pas atteint
        game.player.world_x = max(75, min(WORLD_W - 75, game.player.world_x))
        game.player.world_y = max(0, min(WORLD_H - 30, game.player.world_y))
        # -------- Camera deadzone scrolling --------
        game.update_camera(SCREEN_W, SCREEN_H, WORLD_W, WORLD_H)

        # -------- Game logic --------
        game.update_trash_visibility(SCREEN_W)
        game.try_pickup_trash()
        game.damage()

        # #gravity on trash & plat /gravité des déchets sur les plateformes(ne marche pas pour l'instant)
        for trash in game.all_trash:
            trash.apply_gravity(game.platforms, WORLD_H)

        # transition quand goal atteint
        if game.goal == 0 and not transitioning and not lose:
            transitioning = True
            fading_in = True

        # Animation fondu/fade
        if transitioning:
            if fading_in:
                fade = min(255, fade + 8)
                if fade >= 255:
                    fading_in = False
                    fading_out = True
                    result = game.next_lvl()
                    if result == 'victory':
                        lose = True
                        transitioning = False
                    else:#respawn au debut
                        game.player.world_x = 200
                        game.player.world_y = 2125

            elif fading_out:
                fade = max(0, fade - 8)
                if fade <= 0:
                    fading_out = False
                    transitioning = False
        # check win/lose
        if game.player.health <= 0 and not lose:
            lose = True
            game.pressed = {}
            timer.finished = True  #game over

        # -------- Draw --------
        game.draw_background(screen, bg, COLS, ROWS, CELL_W, CELL_H, SCREEN_W, SCREEN_H)
        game.draw_objects(screen)
        game.draw_ui(screen, lose)
        #starts the timer
        timer.update()
        timer.display_timer(screen)
        timer.display_pause(screen)
        timer.display_game_over(screen)  # s'affiche si timer.finished = True
        #restart and display win/lose
        if lose and game.level >= 3 and game.goal == 0:
            w, h = screen.get_size()
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            font_big = pygame.font.SysFont("consolas", 72, True)
            font_sub = pygame.font.SysFont("consolas", 28)
            win_txt = font_big.render("VICTORY!", True, (80, 255, 150))
            screen.blit(win_txt, win_txt.get_rect(center=(w // 2, h // 2 - 80)))
            sub_txt = font_sub.render("Press R to restart", True, (59, 113, 128))
            screen.blit(sub_txt, sub_txt.get_rect(center=(w // 2, h // 2 + 60)))

        # gestion touche R pour restart
        if fade > 0:
            fade_surface.set_alpha(fade)
            screen.blit(fade_surface, (0, 0))
        pygame.display.flip()


        clock.tick(60)
        """
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

        # ── Arc throw visuals ────────────────────────────────────────────────────
        game.draw_carried_trash(screen)  # draws the actual trash sprite floating above player

        # arc preview and bin highlight while dragging
        mouse_pos = pygame.mouse.get_pos()
        if game.throw_state == "dragging" and game.carrying:
            draw_arc_preview(screen, game, mouse_pos)
            draw_bin_highlight(screen, game, mouse_pos)

        # -------- UI --------
        font = pygame.font.SysFont(None, 40)

        game.player.update_health_bar()
        screen.blit(pygame.transform.scale(game.player.health_image, (120, 50)), (10, 50))

        score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
        # lives_text = font.render(f"Vies: {game.lives}", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))
        # screen.blit(lives_text, (10, 50))

        if game.carrying:
            carry_text = font.render(f"Tu portes : {game.carried_trash_type}", True, (255, 255, 0))
            screen.blit(carry_text, (10, 90))

        if game.player.health == 0:
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
        clock.tick(60)"""



"""# Start the game
menu_choice = main_menu.main_menu(screen)

# credit managment
while menu_choice == "credits":
    credits_choice = main_menu.credits(screen)

    if credits_choice == "back":
        menu_choice = main_menu.main_menu(screen)

    elif credits_choice == "quit":
        pygame.quit()
        exit()"""


"""running = True
camera_x = 0
camera_y = 0
lose = False

while running:
    clock.tick(60)


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

         # ── Throw: drag starts on left click (only when carrying) ──
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            game.start_drag(event.pos)

        # ── Throw: release launches projectile ──
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            game.release_drag(event.pos)

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

    game.update_projectile() #advance projectile physics every frame

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

    # ── Arc throw visuals ────────────────────────────────────────────────────
    game.draw_carried_trash(screen)  # draws the actual trash sprite floating above player

    # arc preview and bin highlight while dragging
    mouse_pos = pygame.mouse.get_pos()
    if game.throw_state == "dragging" and game.carrying:
        draw_arc_preview(screen, game, mouse_pos)
        draw_bin_highlight(screen, game, mouse_pos)

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

    if game.player.health == 0:
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
    clock.tick(60)"""








