import pygame
from classes.game import Game
from classes.timer import Timer
from classes.platform import Platform, MovingPlatform

def level1(screen):
    clock = pygame.time.Clock()
    timer = Timer(600)
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

    #song
    pygame.mixer.music.load("asset/sound/level_1_song.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    game_over_music_playing = False

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
                    game_over_music_playing = False
                    pygame.mixer.music.load("asset/sound/level_1_song.mp3")
                    pygame.mixer.music.set_volume(0.3)
                    pygame.mixer.music.play(-1)

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

        if lose and not game_over_music_playing and not (game.level >= 3 and game.goal == 0):
            pygame.mixer.music.stop()
            pygame.mixer.music.load("asset/sound/game_over_sfx.mp3")
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play()  # pas de -1 : joue une seule fois
            game_over_music_playing = True

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
