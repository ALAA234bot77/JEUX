
import pygame

class Trash(pygame.sprite.Sprite):
    def __init__(self, x, y, trash_type):
        super().__init__()
        self.trash_type = trash_type

        # Forme différente par couleur en attendant les images
        if trash_type == "recyclable":
            original_image = pygame.image.load('asset/trash/plastic.png')   # bleu = plastique
        elif trash_type == "menager":
            original_image = pygame.image.load('asset/trash/menager.png')# gris = sac poubelle
        elif trash_type == "compost":
            original_image = pygame.image.load('asset/trash/apple.png')      # vert = nourriture
        elif trash_type == "paper":
            original_image = pygame.image.load('asset/trash/papier.png')

        elif trash_type == "glass":
            original_image = pygame.image.load('asset/trash/glass.png')

        elif trash_type == "clothing":
            original_image = pygame.image.load('asset/trash/clothing.png')

        self.image = pygame.transform.scale(original_image, (90, 90))
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

