import pygame

class Timer:
    """
    Gère un timer de compte à rebours et
     la pause,le restart et détecte la fin du temps.
    """

    def __init__(self, total_seconds=300):
        # Durée du timer en secondes 5 min = 300s
        self.total_seconds = total_seconds

        # Temps au moment du démarrage de la game en ms
        self.start_ticks = pygame.time.get_ticks()

        # Compte le temps passé en pause en ms
        self.total_paused_ms = 0

        # Temps du début de la pause en cours
        self.pause_start = 0

        # detecte l'etat en pause ou la fin du timer
        self.paused = False
        self.finished = False

        # Temps restant visible en s (mis à jour dans update())
        self.remaining = total_seconds

        # Police d'affichage du timer
        self.font = pygame.font.SysFont("consolas", 36, True)

        # Polices pour la pause et game over
        self.font_big = pygame.font.SysFont("consolas", 72, True)
        self.font_sub = pygame.font.SysFont("consolas", 28)

    #fonction update of the timer
    def update(self):
        """
        Recalcule le temps restant à chaque image.
        (dans le main).
        """
        if self.paused or self.finished:
            return  # pas de calcul(aucun changement de temps) si en pause ou terminé

        # Temps écoulé réel = temps total - temps passé en pause
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks - self.total_paused_ms
        elapsed_seconds = elapsed_ms // 1000  #  ms à secondes(int)

        # Temps restant
        self.remaining = max(0, self.total_seconds - elapsed_seconds)#max pour ne pas avoir de temps negatif

        # Fin du timer si temps rstant = 0
        if self.remaining == 0:
            self.finished = True

    # Fonction mettre en pause au reprendre la partie
    def set_pause(self):
        """
        Changement d'etat entre la pause et la reprise.
        accumule le temps de pause pour ne pas le décompter.
        """
        if self.finished:
            return  # Impossible de mettre en pause si le jeu est terminé.
        #sinon on change d'état (on reprend ou pause la partie en fonction de la valeur de self.paused .
        self.paused = not self.paused #sinon on change d'état (on reprend ou pause la partie en fonction de la valeur de self.paused .

        if self.paused:
            #si l'état devient en pause alors: on note l'instant où la pause commence
            self.pause_start = pygame.time.get_ticks()
        else:
            # si l'état = pas en pause on ajoute la durée deja cumulée de la pause pause au cumul total
            self.total_paused_ms += pygame.time.get_ticks() - self.pause_start

    #fonction recommencer la partie
    def restart(self):
        """
        remet le timer à zéro et relance le compte à rebours.
        """
        self.start_ticks    = pygame.time.get_ticks()  # nouveau temps de départ
        self.total_paused_ms = 0  # cumul des pauses = 0
        self.pause_start    = 0 #
        self.paused         = False #on enleve l'état de pause
        self.finished       = False  #la partie n'est pas finie
        self.remaining      = self.total_seconds        #  le temps restant = temps max

    #AFFICHAGE

    #fonction format du temps en minutes
    def get_format_min(self):
        """
        Retourne le temps restant sous forme minutes:secondes(ex:01;22)
        """
        minutes = self.remaining // 60   # minutes en entiers
        seconds = self.remaining % 60    # secondes restantes
        return f"{minutes:02}:{seconds:02}"  # formate sur 2 chiffres (02)

    #fonction affichage du timer
    def draw_timer(self, screen):
        """
        affiche le timer en haut à gauche de l'écran.
        devient rouge si moins de 30 secondes restantes.
        """
        if self.finished:
            return  # pas d'affichage du timer sur l'écran de game over

        text = self.get_format_min()#récupere le temps sous format"mm:ss" pour l'utilser en texte d'affichage du timer


        if self.remaining <= 30 :# si il reste que 30sec les chiffres du timer sont rouge
            color = (255, 255, 255)#rouge en rgb
        else:
            color = (255, 60, 60)#blanc sinon

        # Crée la surface de texte "mm.ss"
        surface = self.font.render(text, True, color)

        # place le timer en haut à gauche
        screen.blit(surface, (20, 20))

    #fovtion affiche le bouton pause
    def draw_pause_overlay(self, screen):
        """
        Affiche un écran un pru transparent avec ecrit par dessus "PAUSE".
        """
        if not self.paused:
            return  # rien ne se passe si pas en pause

        w, h = screen.get_size()  # dimensions de l'écran

        # Surface transparente de la même taille que l'écran
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))  # noir à 55% d'opacité
        screen.blit(overlay, (0, 0))

        # texte "PAUSE" centré
        pause_txt = self.font_big.render("PAUSE", True, (100, 255, 150))#message pause couleur
        pause_rect = pause_txt.get_rect((w // 2, h // 2 - 50))#met au centre
        screen.blit(pause_txt, pause_rect)

        # Sous-titre
        sub_txt = self.font_sub.render("Press C to continue", True, (200, 200, 200))#messsage sous titre couleur
        sub_rect = sub_txt.get_rect((w // 2, h // 2 + 30))
        screen.blit(sub_txt, sub_rect)

    #fonction affichage game over
    def draw_game_over_overlay(self, screen):
        """
        affiche l'écran de fin de partie avec option de rejouer.
        """
        if not self.finished:
            return  # rien si le jeu n'est pas terminé

        w, h = screen.get_size()#taille de l'ecran

        # fond tqnsparent 70 opacité
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)#transparence
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # affiche "GAME OVER" en rouge
        go_txt = self.font_big.render("GAME OVER", True, (255, 70, 70))#texte game over rouge
        go_rect = go_txt.get_rect((w // 2, h // 2 - 80))
        screen.blit(go_txt, go_rect)#affiche leteste go txt a la place go_rect

        # sous titre
        sub_txt = self.font_sub.render("Time is over!", True, (200, 200, 200))
        sub_rect = sub_txt.get_rect((w // 2, h // 2))
        screen.blit(sub_txt, sub_rect)

        #Rajouter texte si toutes les vies sont perdues

        # recommencer
        replay_txt = self.font_sub.render("press R to restart", True, (255, 200, 100))
        replay_rect = replay_txt.get_rect((w // 2, h // 2 + 60))
        screen.blit(replay_txt, replay_rect)



