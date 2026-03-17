import pygame
from game import Game
from player import Player
"""This is the main program"""
pygame.init()

clock = pygame.time.Clock()
clock.tick(60)

SCREEN_W, SCREEN_H = 1080, 720
pygame.display.set_caption("Trash Cat 67")
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))

# ── WORLD SETTINGS (just change these two numbers to resize later) ──
COLS = 0
ROWS = 3
CELL_W = 1080
CELL_H = 720
WORLD_W = COLS * CELL_W  # 3240
WORLD_H = ROWS * CELL_H  # 2160

# ── LOAD BACKGROUND GRID ───────────────────────────────────────────
# Expected filenames: asset/bg_0_0.jpg, asset/bg_1_0.jpg, etc.
# col = left to right (0,1,2), row = top to bottom (0,1,2)
bg = {}
for col in range(COLS):
    for row in range(ROWS):
        img = pygame.image.load(f'asset/bg_{col}_{row}.jpg')
        bg[(col, row)] = pygame.transform.scale(img, (CELL_W, CELL_H))
#charger le jeux
game = Game()
running = True


while running:

    #appliquer la fenetre de jeu
    screen.blit(background,(0,0))
    game.update_camera()
    game.update_trash_visibility()
    for trash in game.visible_trash:
        screen_x = trash.rect.x - game.camera_x
        screen.blit(trash.image, (screen_x, trash.rect.y))
    font = pygame.font.SysFont(None, 40)
    score_text = font.render(f"Score: {game.score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))



    # ── CLAMP PLAYER TO WORLD EDGES ────────────────────────────────
    game.player.world_x = max(75, min(WORLD_W - 75, game.player.world_x))
    game.player.world_y = max(0, min(WORLD_H - 30, game.player.world_y))

    # ── CAMERA: follow player, clamped to world boundaries ─────────
    # ── CAMERA with edge-scroll deadzone ──────────────────────────────
    SCROLL_MARGIN = 200  # how close to screen edge before camera moves

    # Horizontal scroll
    player_screen_x = game.player.world_x - camera_x

    if player_screen_x > SCREEN_W - SCROLL_MARGIN:
        camera_x = game.player.world_x - (SCREEN_W - SCROLL_MARGIN)
    elif player_screen_x < SCROLL_MARGIN:
        camera_x = game.player.world_x - SCROLL_MARGIN

    # Vertical scroll
    player_screen_y = game.player.world_y - camera_y
    if player_screen_y > SCREEN_H - SCROLL_MARGIN:
        camera_y = game.player.world_y - (SCREEN_H - SCROLL_MARGIN)

    elif player_screen_y < SCROLL_MARGIN:
        camera_y = game.player.world_y - SCROLL_MARGIN

    # Clamp camera to world boundaries
    camera_x = max(0, min(WORLD_W - SCREEN_W, camera_x))
    camera_y = max(0, min(WORLD_H - SCREEN_H, camera_y))

    camera_x = max(0, min(WORLD_W - SCREEN_W, camera_x))
    camera_y = max(0, min(WORLD_H - SCREEN_H, camera_y))

    # ── DRAW BACKGROUND CELLS ──────────────────────────────────────
    for col in range(COLS):
        for row in range(ROWS):
            screen_x = col * CELL_W - camera_x
            screen_y = row * CELL_H - camera_y
            if (-CELL_W < screen_x < SCREEN_W) and (-CELL_H < screen_y < SCREEN_H):
                screen.blit(bg[(col, row)], (screen_x, screen_y))

    # ── SYNC PLAYER rect TO SCREEN POSITION ────────────────────────
    game.player.rect.centerx = int(game.player.world_x - camera_x)
    game.player.rect.bottom = int(game.player.world_y - camera_y)



    #appliquer l'image du joueur
    screen.blit(game.player.image, game.player.rect)

    #verifier si on va gauche ou droite:
    if game.pressed.get(ord('d')) and game.player.rect.x < 950:
        game.player.move_right()
    if game.pressed.get(ord('q')) and game.player.rect.x > 0:
        game.player.move_left()

    if game.pressed.get(pygame.K_SPACE) or game.pressed.get(ord('s')):
        game.player.jump()

    game.player.apply_gravity()
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

        #decter si le jouer lache une touch
        elif event.type == pygame.KEYDOWN:#quel touche etait appuile
            game.pressed[event.key] = True



        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False

    clock.tick(60)
