import pygame
from random import randint
from VAISSEAU.vaisseau_mere import Vaisseau # import du vaisseau mère
from ENNEMIES.ennemies_vaisseau_mere import Ennemie # import des ennemies
from PROTECTION.protections_vaisseau_mere import Protection # import des protections
from TIRES.tire import Tire

from information_jeu import * # toutes les informations du jeu

from typing import Union
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

        self.__tir: Union[Tire, None] = None # le tir en cour
        self.__ennemies_tirs: list[Tire] = [] # la liste des tirs des ennemies

        self.__event_attente_ennemie = pygame.event.custom_type()
        pygame.time.set_timer(self.__event_attente_ennemie, 900)
        self.__event_count: int = 0
        self.__event_direction: int = 5

        self.__event_attente_tires = pygame.event.custom_type()
        pygame.time.set_timer(self.__event_attente_tires, 100)

        self.__protections = Protection.creer_protections(screen, nb_protections=4, y_position=370) # creer 3 protections avec la position horizontale

        self.__tir_ennemie_aleatoire: int = 50

        self.__texte_surface = pygame.font.Font(size=100)


        self.score = 0 ##On initialise le score à 0 au début de la partie
        self.score_font = pygame.font.Font('Fontscore.ttf',25) ##on défini la police d'écriture et la taille de l'affichage du score
        self.score_position = [10,10] ##position du score
        



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

                elif touche == 'm':
                    self.__tir_ennemie_aleatoire //= 2

                elif touche == ' ': # si la barre espace est activé
                    if self.__tir is None:
                        self.__tir = self.__vaisseau.tirer()

                else: # si on ne bouge pas le vaisseau mère, on met sa vitesse à 0
                    self.__vaisseau.vitesse = 0

            if event.type == self.__event_attente_ennemie: # EVENT QUI FAIT BOUGER LES ENNEMIES

                liste_ennemie = []
                for ennemie in range(len(self.__ennemies)):
                    if not self.__ennemies[ennemie].vie:
                        liste_ennemie.append(ennemie)
                    self.__ennemies[ennemie].x = self.__ennemies[
                                                     ennemie].x + self.__event_direction  ##TRANSFORMER EN LISTE POUR LES SUPPRIMER A LA MORT

                    if self.__ennemies[ennemie].vie and randint(0, self.__tir_ennemie_aleatoire) == 0: # tire aléatoire des ennemies
                        self.__ennemies_tirs.append(self.__ennemies[ennemie].tirer())

                self.__event_count += 1  ##rajouter un "if ennemie.mort ou un truc du style"

                ##mais tkt c'est facile
                if self.__event_count > 3:
                    self.__event_direction *= -1
                    self.__event_count = 0

                for ennemie2 in range(len(self.__ennemies)):
                    if ennemie2 in liste_ennemie:
                        self.__ennemies.pop(ennemie2)
                        self.score += 10 ##ajoute 10 au score du joueur



            if event.type == self.__event_attente_tires: # EVENT QUI FAIT BOUGER LES TIRS
                
                for ennemie in self.__ennemies: # itère sur tous les ennemies

                    if self.__tir is not None and self.__tir.collision(ennemie): # si il existe un tir et qu'il y a une collision (l'affichage de l'ennemie est désactivé dans self.__tire.collision
                        self.__tir = None # on retire le tire

                # Gestion des collisions entre le tir du vaisseau et les protections
                if self.__tir is not None:
                    for protection in self.__protections:
                        if protection.vie and self.__tir._Tire__rect.colliderect(protection.rect):
                            protection.degats()  # La protection prend des dégâts
                            self.__tir = None  # On retire le tir après la collision
                            break  # Sortir de la boucle après une collision

                if self.__tir is not None: # s' il existe un tire
                    self.__tir.y = self.__tir.y - 35 # on le fait bouger

                new_tirs = []
                for tir_ennemie in self.__ennemies_tirs: # iter sur tous les tirs des ennemies
                    collision_detectee = False

                    for protection in self.__protections:
                        if tir_ennemie._Tire__rect.colliderect(protection.rect) and protection.vie:
                            protection.degats()  # La protection prend des dégâts
                            collision_detectee = True  # Le tir s'arrête après avoir touché la protection
                            break
                    if not collision_detectee:
                        if tir_ennemie.collision(self.__vaisseau):  
                            self.__vaisseau.vie -= 1  # Réduit la vie du vaisseau

                                # Affiche une explosion temporaire
                            explosion = pygame.image.load("VAISSEAU\Assets\space__0010_PlayerExplosion.png")  # image d'explosion
                            screen.blit(explosion, (self.__vaisseau.x, self.__vaisseau.y))


                            if self.__vaisseau.vie <= 0:
                                self.__defaite()


                        
                        else: # sinon
                            tir_ennemie.y = tir_ennemie.y + 15
                            new_tirs.append(tir_ennemie)

                self.__ennemies_tirs = new_tirs.copy()





            if event.type == pygame.QUIT:
                running = False



    def affichage(self) -> None:
        """
        Affiche tous le contenue du jeu frame par frame
        :return:
        """

        if self.__tir is not None:
            self.__tir.afficher_tire()

        for tir in self.__ennemies_tirs:
            tir.afficher_tire()

        self.__vaisseau.afficher_vaisseau()

        for ennemie in self.__ennemies:
            ennemie.afficher_ennemie()

        for protection in self.__protections:
            protection.afficher_protection()

        if len(self.__ennemies) == 0:
            self.__victoire()

        self.score_affichage = self.score_font.render("Score : "+ str(self.score),1,(255,255,255)) ##met à jour le contenu (score) à afficher à l'écran
        screen.blit((self.score_affichage), self.score_position) ##affiche le score mis à jour
        
        # Affichage des vies
        self.vies_affichage = self.score_font.render("Vies : " + str(self.__vaisseau.vie), 1, (255, 255, 255))# comme pour le score
        screen.blit(self.vies_affichage, [400, 10])  # affiche la vie a coté du score


    def __victoire(self):
        """
        Affiche un écran de fin si le joueur a gagné
        :return:
        """
        texte = pygame.font.Font.render(self.__texte_surface, "VICTOIRE !", 1, (255,255,255))
        r = texte.get_rect()
        r.x = window_longueur/2 - r.centerx
        r.y = window_largeur/2 - r.centery
        screen.blit(texte, r)
        
    def __defaite(self):
        """
        Affiche un écran de défaite et ferme le jeu
        """
        texte = pygame.font.Font.render(self.__texte_surface, "DEFAITE", 1, (255, 0, 0))
        r = texte.get_rect()
        r.x = window_longueur / 2 - r.centerx
        r.y = window_largeur / 2 - r.centery
        screen.blit(texte, r)
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause de 3 secondes avant de quitter
        pygame.quit()# ferme le jeux
        exit()



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
                ennemies.append(Ennemie(screen, x, y, self.__select_animation_ennemie(ligne)))

        return ennemies

    def __select_animation_ennemie(self, ligne: int) -> tuple[str, str]:
        """
        Sélectionne les 2 images d'animation pour la ligne en question
        :param ligne: la ligne d'ennemie actuellement en création
        :return:
        """
        annim_lignes = {
            1: ('space__0004_C1.png', 'space__0005_C2.png'),
            2: ('space__0002_B1.png', 'space__0003_B2.png'),
            3: ('space__0000_A1.png', 'space__0001_A2.png')
        }

        if ligne >= 3:
            return annim_lignes[3]

        elif 2 >= ligne >= 1:
            return annim_lignes[2]

        else:
            return annim_lignes[1]
        

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
