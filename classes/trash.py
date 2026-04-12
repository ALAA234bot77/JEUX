
import pygame

class Trash(pygame.sprite.Sprite):
    def __init__(self, x, y, trash_type):
        super().__init__()
        self.trash_type = trash_type

        # Forme différente par couleur en attendant les images
        if trash_type == "recyclable":
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 100, 255))    # bleu = plastique
        elif trash_type == "menager":
            self.image = pygame.Surface((35, 50))
            self.image.fill((100, 100, 100))  # gris = sac poubelle
        elif trash_type == "compost":
            self.image = pygame.Surface((40, 40))
            self.image.fill((0, 180, 0))      # vert = nourriture
        elif trash_type == "paper":
            self.image = pygame.Surface((50, 35))
            self.image.fill((255, 220, 0))    # jaune = journal
        elif trash_type == "glass":
            self.image = pygame.Surface((30, 55))
            self.image.fill((0, 200, 200))    # cyan = bouteille
        elif trash_type == "clothing":
            self.image = pygame.Surface((50, 40))
            self.image.fill((200, 0, 200))    # violet = t-shirt

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y

        # Position monde pour
        self.world_x = float(self.rect.centerx)
        self.world_y = float(y)
        self.fall_velocity = 0
        self.gravity = 0.6
        self.on_ground = False

    def apply_gravity(self, platforms, world_h):
        if self.on_ground:
            return

        self.fall_velocity += self.gravity
        self.world_y += self.fall_velocity
        # Sol
        if self.world_y >= world_h - 30:
            self.world_y = world_h - 30
            self.fall_velocity = 0
            self.on_ground = True

