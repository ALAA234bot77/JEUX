import pygame

class Bin(pygame.sprite.Sprite):
    def __init__(self, x, bin_type):
        super().__init__()
        self.bin_type = bin_type

        # Couleur selon le type de poubelle
        if bin_type == "recyclable":
            self.color = (0, 0, 255)      # 🔵 bleu
        elif bin_type == "menager":
            self.color = (255, 0, 0)      # 🔴 rouge
        elif bin_type == "compost":
            self.color = (0, 200, 0)      # 🟢 vert
        elif bin_type == "papier":
            self.color = (255, 255, 0)    # 🟡 jaune
        elif bin_type == "verre":
            self.color = (0, 200, 200)    # 🫙 cyan
        elif bin_type == "vetement":
            self.color = (150, 0, 200)    # 👕 violet

        self.image = pygame.Surface((60, 80))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = 690  # posée au sol
