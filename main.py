import pygame
from VAISSEAU.vaisseau_mere import Vaisseau # import du vaisseau mère
from ENNEMIES.ennemies_vaisseau_mere import Ennemie # import des ennemies

from information_jeu import * # toutes les informations du jeu
"""
Information du jeu trouvable dans information_jeu.py
"""


# pygame setup
pygame.init()
screen = pygame.display.set_mode((window_longueur, window_largeur))
clock = pygame.time.Clock()
running = True



class Jeu:

    def __init__(self):
        """
        Initialisation du jeu
        """
        self.__vaisseau: Vaisseau = Vaisseau(vaisseau_posX, vaisseau_posY, screen) # le vaisseau contrôlé par le joueur

        self.__ennemies: list[Ennemie] = self.__split_ennemies() # sépare les ennemies de façon équitable sur plusieurs lignes


    def event(self) -> None:
        """
        Gère la venue des évènement pygame
        :return: None
        """
        global running
        #print(pygame.event.get())
        for event in pygame.event.get(): # récupère la liste des évènements

            """
            Déplacement du vaisseau mère de gauche à droite
            """
            if 'text' in event.dict: # regarde si la clée "text" est dans le dict des données de l'event

                if event.dict['text'] == 'q': # si la touche Q est activé
                    self.__vaisseau.vitesse = -5

                elif event.dict['text'] == 'd': # si la touche D est activé
                    self.__vaisseau.vitesse = 5

                else: # si on ne bouge pas le vaisseau mère, on met sa vitesse à 0
                    self.__vaisseau.vitesse = 0

            if event.type == pygame.QUIT:
                running = False


    def affichage(self) -> None:
        """
        Affiche tous le contenue du jeu frame par frame
        :return:
        """
        self.__vaisseau.afficher_vaisseau()


        for ennemie in self.__ennemies:

            ennemie.afficher_ennemie()


    def __split_ennemies(self) -> list[Ennemie]:
        """
        Sépare les ennemies sur la carte en une grille de lignes * colonnes
        :return:
        """
        ennemies = []


        # Création des 50 instances
        for ligne in range(lignes):  # x lignes
            for colonne in range(colonnes):  # x colonnes
                x = colonne * espacement_collone + rayon_ennemie + 5
                y = ligne * espacement_ligne + rayon_ennemie + 5
                ennemies.append(Ennemie(screen, x, y, rayon_ennemie))

        return ennemies


jeu = Jeu() # initialisation du jeu

while running:

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    jeu.event() # gère tous les évènements
    jeu.affichage() # gère l'affichage du jeu

    # flip() affiche le contenue à l'écran
    pygame.display.flip()

    clock.tick(FPS)  # 25 fps

pygame.quit()
