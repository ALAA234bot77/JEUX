import pygame

class Bin(pygame.sprite.Sprite):
    def __init__(self, x, y, bin_type):
        super().__init__()

        self.bin_type = bin_type

        # Couleur selon le type de poubelle
        if bin_type == "recyclable":
            original_image = pygame.image.load('asset/bin/bin_1.png')
            #self.color = (0, 0, 255)      # 🔵 bleu
        elif bin_type == "menager":
            original_image = pygame.image.load('asset/bin/bin_5.png')
            #self.color = (255, 0, 0)      # 🔴 rouge
        elif bin_type == "compost":
            original_image = pygame.image.load('asset/bin/bin_3.png')
            #self.color = (0, 200, 0)      # 🟢 vert
        elif bin_type == "papier":
            original_image = pygame.image.load('asset/bin/bin_4.png')
            #self.color = (255, 255, 0)    # 🟡 jaune
        elif bin_type == "verre":
            original_image = pygame.image.load('asset/bin/bin_2.png')
            #self.color = (0, 200, 200)    # 🫙 cyan
        elif bin_type == "vetement":
            original_image = pygame.image.load('asset/bin/bin_6.png')
            #self.color = (150, 0, 200)    # 👕 violet"""

        #self.image = pygame.Surface((60, 80))
        #self.image.fill(self.color)
        self.image = pygame.transform.scale(original_image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
