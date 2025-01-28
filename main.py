import pygame
from VAISSEAU.vaisseau_mere import Vaisseau # import du vaisseau mère
from ENNEMIES.ennemies_vaisseau_mere import Ennemie # import des ennemies
from TIRES.tire import Tire

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

        self.__tires: list[Tire] = [] # La liste de tire en cours dans le jeu

        self.__event_attente_ennemie = pygame.event.custom_type()
        pygame.time.set_timer(self.__event_attente_ennemie, 900)
        self.__event_count: int = 0
        self.__event_direction: int = 5

        self.__event_attente_tires = pygame.event.custom_type()
        pygame.time.set_timer(self.__event_attente_tires, 100)


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

                touche: str = event.dict['text']

                if touche == 'q': # si la touche Q est activé
                    self.__vaisseau.vitesse = -vaisseau_vitesse

                elif touche == 'd': # si la touche D est activé
                    self.__vaisseau.vitesse = vaisseau_vitesse

                elif touche == ' ': # si la barre espace est activé
                    self.__tires.append(self.__vaisseau.tirer())

                else: # si on ne bouge pas le vaisseau mère, on met sa vitesse à 0
                    self.__vaisseau.vitesse = 0

            if event.type == self.__event_attente_ennemie:
                
                liste_ennemie = []
                for ennemie in range(len(self.__ennemies)):
                    if not self.__ennemies[ennemie].vie:
                        liste_ennemie.append(ennemie)
                    self.__ennemies[ennemie].x = self.__ennemies[ennemie].x + self.__event_direction ##TRANSFORMER EN LISTE POUR LES SUPPRIMER A LA MORT
                self.__event_count += 1                            ##rajouter un "if ennemie.mort ou un truc du style"
                                                                   ##mais tkt c'est facile
                if self.__event_count > 3:
                    self.__event_direction *= -1
                    self.__event_count = 0
                for ennemie2 in range(len(self.__ennemies)):
                    if ennemie2 in liste_ennemie:
                        self.__ennemies.pop(ennemie2)

            if event.type == self.__event_attente_tires:
                
                liste_tirs_touche = []
                for tire in range(len(self.__tires)): #on itère sur tous les tirs en cours (A REMPLACER PAR UN SEUL TIR)
                    
                    for ennemie in self.__ennemies: # on itère sur chaque ennemie
                        
                        if not self.__tires[tire].collision(ennemie): # s'il n'y a pas eu de collision
                            self.__tires[tire].y = self.__tires[tire].y - 1 # on fait avancer le tir
                        else:
                            liste_tirs_touche.append(tire) # sinon on l'ajoute à la liste des tirs à retirer pour la prochaine frame
                            
                for tire2 in range(len(self.__tires)): # on iter sur les tirs
                    if tire2 in liste_tirs_touche: # s'il est dans les tirs à retirer
                        self.__tires.pop(tire2) # on l'enlève de la liste des tirs en cours
                                   





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

        for tire in self.__tires:
            tire.afficher_tire()


    def __split_ennemies(self) -> list[Ennemie]:
        """
        Sépare les ennemies sur la carte en une grille de lignes * colonnes
        :return:
        """
        ennemies = []


        # Création des 50 instances
        for ligne in range(lignes):  # x lignes
            for colonne in range(colonnes):  # x colonnes
                x = colonne * espacement_collone + rayon_ennemie
                y = ligne * espacement_ligne + rayon_ennemie + 40
                ennemies.append(Ennemie(screen, x, y))

        return ennemies


jeu = Jeu() # initialisation du jeu

while running:

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    jeu.event() # gère tous les évènements
    jeu.affichage() # gère l'affichage du jeu

    # flip() affiche le contenue à l'écran
    pygame.display.flip()

    clock.tick(FPS)  # fps

pygame.quit()
