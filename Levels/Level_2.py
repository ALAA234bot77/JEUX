import pygame
from classes.game import Game


def level2(screen):
    clock = pygame.time.Clock()

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

            elif event.type == pygame.KEYUP:
                game.pressed[event.key] = False

            # ── Throw: drag starts on left click (only when carrying) ──
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game.start_drag(event.pos)

            # ── Throw: release launches projectile ──
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                game.release_drag(event.pos)

        # -------- Player movement in world coordinates --------
        if not lose:  # when game over you can move but the game don't close instantly
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
        game.player.world_x = max(75, min(WORLD_W - 75, game.player.world_x))
        game.player.world_y = max(0, min(WORLD_H - 30, game.player.world_y))

        # -------- Camera deadzone scrolling --------
        game.update_camera(SCREEN_W, SCREEN_H, WORLD_W, WORLD_H)

        # -------- Game logic --------
        game.update_trash_visibility(SCREEN_W)
        game.try_pickup_trash()
        game.damage()

        # -------- Check win/lose --------
        if game.player.health <= 0:
            lose = True
        if game.next_lvl() == 'Victory':
            lose = True

        # -------- Draw --------
        game.draw_background(screen, bg, COLS, ROWS, CELL_W, CELL_H, SCREEN_W, SCREEN_H)
        game.draw_objects(screen)
        game.draw_ui(screen, lose)

        pygame.display.flip()
        clock.tick(60)
