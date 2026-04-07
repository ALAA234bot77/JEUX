import pygame
class Timer:
    """
    Gère un timer de compte à rebours et
     la pause,le restart et détecte la fin du temps.
    """
    #
    def __init__(self, total_seconds=300):
        # Durée du timer en secondes 5 min = 300s
        # Duration of the timer 5 min = 300s
        self.total_seconds = total_seconds

        # Temps au moment du démarrage de la game en ms
        # Time at the moment of the start of the game
        self.start_ticks = pygame.time.get_ticks()

        # Compte le temps passé en pause en ms
        # CV+ount the elapsed time during th pause
        self.total_paused_ms = 0

        # Temps du début de la pause en cours
        #Time at the start the pause = 0 because not started yet
        self.pause_start = 0

        # detecte l'etat en pause ou la fin du timer
        # detect the state (paused ou finished)
        self.paused = False
        self.finished = False

        # Temps restant visible en s (mis à jour dans update())
        # Remainig sec(updated at every sec in Update()
        self.remaining = total_seconds

        # Police d'affichage du timer
        #Font of the timer text
        self.font = pygame.font.SysFont("consolas", 36, True)

        # Polices pour la pause et game over
        #font for pause and game over
        self.font_big = pygame.font.SysFont("consolas", 72, True)
        self.font_sub = pygame.font.SysFont("consolas", 28)

    #fonction update of the timer
    def update(self):
        """
        Recalcule le temps restant à chaque image.
        (dans le main).

        Compute the remaining time at every frame(in main)
        """
        if self.paused or self.finished:
            #nothing if in pause of finished
            return  # pas de calcul(aucun changement de temps) si en pause ou terminé

        # Temps écoulé réel = temps total - temps passé en pause
        # real ellapsed time  = total time - time elapsed during the pause
        elapsed_ms = pygame.time.get_ticks() - self.start_ticks - self.total_paused_ms
        elapsed_seconds = elapsed_ms // 1000  #  ms à secondes(int)

        # Temps restant
        # remaining time
        #we use max to not have a negative value for the time
        self.remaining = max(0, self.total_seconds - elapsed_seconds)#max pour ne pas avoir de temps negatif

        # Fin du timer si temps rstant = 0
        #end of the timer if remaining time =0
        if self.remaining == 0:
            self.finished = True

    # Fonction mettre en pause au reprendre la partie
    # function set in pause or continue the game
    def set_pause(self):
        """
        Changement d'etat entre la pause et la reprise.
        accumule le temps de pause pour ne pas le décompter.

        Change the state beteween the pause and the restart.
        accumulate the time during the pause to not get it of from the remaining time
        """
        if self.finished:
            return  # Impossible de mettre en pause si le jeu est terminé./if finished nothing
        # else we change the state(we restart or pause the game in function of the value of self.paused
        self.paused = not self.paused #sinon on change d'état (on reprend ou pause la partie en fonction de la valeur de self.paused .

        if self.paused:
            #si l'état devient en pause alors: on note l'instant où la pause commence
            #if the state -> pause : we note the moment when pause starts
            self.pause_start = pygame.time.get_ticks()
        else:
            # si l'état = pas en pause on ajoute la durée deja cumulée de la pause pause au cumul total
            #if state = not paused, we add duration already cumlated of the pause to the total cumul
            self.total_paused_ms += pygame.time.get_ticks() - self.pause_start

    #fonction recommencer la partie
    #function restart the game
    def restart(self):
        """
        remet le timer à zéro et relance le compte à rebours.

        Set back the timer at 0 and restart the couter for the restart
        """
        self.start_ticks = pygame.time.get_ticks()  # nouveau temps de départ/new start
        self.total_paused_ms = 0  # cumul des pauses = 0
        self.pause_start = 0 #
        self.paused = False #on enleve l'état de pause/ we change the pause state
        self.finished = False  #la partie n'est pas finie/game not finished
        self.remaining = self.total_seconds#  le temps restant = temps max/remainig time = max time

    #AFFICHAGE
    #DISPLAY

    #fonction format du temps en minutes
    #function
    def get_format_min(self):
        """
        Retourne le temps restant sous forme minutes:secondes(ex:01:22)

        Return the remaining time in minutes:secondes(ex:01:22).
        """
        minutes = self.remaining // 60   # minutes en entiers/min in int
        seconds = self.remaining % 60    # secondes restantes/remaining sec
        return f"{minutes:02}:{seconds:02}"  # formate sur 2 chiffres (02)#formate on 2 numbers

    #fonction affichage du timer
    def display_timer(self, screen):
        """
        affiche le timer en haut à gauche de l'écran.
        devient rouge si moins de 30 secondes restantes.

        Display the timer at the left corner
        becomes red when the remainig time is 30sec
        """
        if self.finished:
            #nothing if game=finished
            return  # pas d'affichage du timer sur l'écran de game over

        text = self.get_format_min()#récupere le temps sous format"mm:ss" pour l'utilser en texte d'affichage du timer
        # get time format "mm:ss" to use it as the displaying txt of the timer

        #if 30 sec remaining timer becomes red
        if self.remaining <= 30 :# si il reste que 30sec les chiffres du timer sont rouge
            color = (143, 25, 21)#rouge en rgb/red
        else:
            color = (245, 245, 245)#blanc sinon/white

        # Crée la surface de texte "mm.ss"
        #create the surface of the txt
        surface = self.font.render(text, True, color)

        # place le timer en haut à gauche
        screen.blit(surface, (20, 20))

    #fovtion affiche le bouton pause
    #function display pause bouton
    def display_pause(self, screen):
        """
        Affiche un écran un peu transparent avec ecrit par dessus "PAUSE".

        displays a transparent screen with pause written on
        """
        if not self.paused:
            #nothing if in pause
            return  # rien ne se passe si pas en pause

        w, h = screen.get_size()  # dimensions de l'écran

        # Surface transparente de la même taille que l'écran
        # transparent surface same dilesion of the screen
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))  # noir à 55% d'opacité
        screen.blit(overlay, (0, 0))

        # texte "PAUSE" centré
        pause_txt = self.font_big.render("PAUSE", True, (115, 170, 186))#message pause couleur
        pause_rect = pause_txt.get_rect(center = (w // 2, h // 2 - 50))#met au centre
        screen.blit(pause_txt, pause_rect)

        # Sous-titre
        sub_txt = self.font_sub.render("Press C to continue", True, (59, 113, 128))#messsage sous titre couleur
        sub_rect = sub_txt.get_rect(center = (w // 2, h // 2 + 30))
        screen.blit(sub_txt, sub_rect)

    #fonction affichage game over
    #function display
    def display_game_over(self, screen):
        """
        affiche l'écran de fin de partie avec option de rejouer.

        Displays the game over screen with restart option
        """
        if not self.finished:
            return  # rien si le jeu n'est pas terminé

        w, h = screen.get_size()#taille de l'ecran/dimension of the screen

        # fond transparent 70 opacité
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)#transparence
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        # affiche "GAME OVER" en rouge
        go_txt = self.font_big.render("GAME OVER", True, (143, 25, 21))#texte game over rouge
        go_rect = go_txt.get_rect(center = (w // 2, h // 2 - 80))
        screen.blit(go_txt, go_rect)#affiche le texte go_txt à la place go_rect

        # sous titresub tiltle
        sub_txt = self.font_sub.render("Time is over!", True, (200, 200, 200))
        sub_rect = sub_txt.get_rect(center = (w // 2, h // 2))
        screen.blit(sub_txt, sub_rect)

        #Rajouter texte si toutes les vies sont perdues
        #add txt when no more hp

        # recommencer/restart
        replay_txt = self.font_sub.render("Press R to restart", True, (59, 113, 128))
        replay_rect = replay_txt.get_rect(center = (w // 2, h // 2 + 60))
        screen.blit(replay_txt, replay_rect)



