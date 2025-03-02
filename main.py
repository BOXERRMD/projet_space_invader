import pygame
from random import randint
from VAISSEAU.vaisseau_mere import Vaisseau # import du vaisseau mère
from ENNEMIES.ennemies_vaisseau_mere import Ennemie # import des ennemies
from PROTECTION.protections_vaisseau_mere import Protection # import des protections
from TIRES.tire import Tire # beaucoup de tirs pour pas grand chose finalement :/ Mais vous savez, moi je ne crois pas qu'il y ait de bonnes ou de mauvaises situations. Moi, si je devais résumer ma vie, aujourd’hui avec vous, je dirais que c’est d´abord des rencontres, des gens qui m’ont tendu la main peut-être à un moment où je ne pouvais pas, où j’étais seul chez moi. Et c’est assez curieux de se dire que les hasards, les rencontres forgent une destinée. Parce que quand on a le goût de la chose, quand on a le goût de la chose bien faite, le beau geste, parfois on ne trouve pas l’interlocuteur en face, je dirais le miroir qui vous aide à avancer. Alors ce n’est pas mon cas, comme je disais là, puisque moi au contraire j’ai pu, et je dis merci à la vie, je lui dis merci, je chante la vie, je danse la vie, je ne suis qu’amour. Et finalement quand beaucoup de gens aujourd’hui me disent : « Mais comment fais-tu pour avoir cette humanité ? » eh bien je leur réponds très simplement, je leur dis : « C’est ce goût de l´amour », ce goût donc, qui m’a poussé aujourd’hui à entreprendre une construction mécanique, mais demain qui sait ? Peut-être simplement à me mettre au service de la communauté, à faire le don, le don de soi.

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

        self.__tir: Union[Tire, None] = None # le tir en cour du vaisseau
        self.__ennemies_tirs: list[Tire] = [] # la liste des tirs des ennemies

        self.__event_attente_ennemie = pygame.event.custom_type() # event pour faire bouger periodiquement les ennemies
        pygame.time.set_timer(self.__event_attente_ennemie, 900) # réglé sur 900ms
        self.__event_count: int = 0 # nombre de fois que les ennemies ont bougé dans une direction
        self.__event_direction: int = 5 # direction et vitesse des ennemies

        self.__event_attente_tires = pygame.event.custom_type() # event pour faire bouger periodiquement les tirs
        pygame.time.set_timer(self.__event_attente_tires, 100) # réglé à 100ms

        self.__protections = Protection.creer_protections(screen, nb_protections=4, y_position=370) # creer 3 protections avec la position horizontale

        self.__tir_ennemie_aleatoire: int = 50 # 1 chance sur X qu'un ennemie puisse tirer. Ici 1/50

        self.__texte_surface = pygame.font.Font(size=100) # initialisation du texte

        self.delai_explosion = None # le délait de l'explosion du vaisseau (qui sera un évènement quand le vaisseau se fera toucher)


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
                    if not self.__ennemies[ennemie].vie: # si l'ennemie est mort
                        liste_ennemie.append(ennemie)
                    self.__ennemies[ennemie].x = self.__ennemies[
                                                     ennemie].x + self.__event_direction  ##TRANSFORMER EN LISTE POUR LES SUPPRIMER A LA MORT

                    if self.__ennemies[ennemie].vie and randint(0, self.__tir_ennemie_aleatoire) == 0: # tire aléatoire des ennemies s'il sont en vie
                        self.__ennemies_tirs.append(self.__ennemies[ennemie].tirer()) # on ajoute le tir dans la liste des tirs ennemie

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
                    self.__tir.y = self.__tir.y - 35  # on fait bouger le tir du vaisseau
                    for protection in self.__protections:
                        if protection.vie and self.__tir._Tire__rect.colliderect(protection.rect): # si colision entre la protection et le tire du vaisseau + la protection est en vie
                            protection.degats()
                            self.__tir = None
                            break


                new_tirs = []
                for tir_ennemie in self.__ennemies_tirs:
                    collision_detectee = False # colision d'un tir sur les protection

                    for protection in self.__protections:
                        if tir_ennemie._Tire__rect.colliderect(protection.rect) and protection.vie: # s'il y a colision avec une protection et  que la protection est en vie
                            protection.degats()  # La protection prend des dégâts
                            collision_detectee = True  # Le tir s'arrête après avoir touché la protection (par défaut)
                            break
                    if not collision_detectee:
                        if tir_ennemie.collision(self.__vaisseau):  
                            

                            # Affiche une explosion temporaire
                            self.__vaisseau.est_touche()
                            self.delai_explosion = pygame.event.custom_type() # set un évènement pour l'affichage du vaisseau explosé
                            pygame.time.set_timer(self.delai_explosion, 200)


                            if self.__vaisseau.vie <= 0: # si la vie du vaisseau déscend à 0 ou moins
                                self.__defaite() # on affiche l'écran de fin


                        
                        else:
                            # Permet de faire avancer les tires et d'append les tirs toujours en cours dans une liste
                            tir_ennemie.y = tir_ennemie.y + 15
                            new_tirs.append(tir_ennemie)

                self.__ennemies_tirs = new_tirs.copy() # on met une copie des tirs encore valide dans la variable des tirs ennemies


            if event.type == self.delai_explosion: # si l'event associé à l'explosion du vaisseau est rencontré
                self.__vaisseau.touche = False # on modifie la valeur du vaisseau touché
                self.delai_explosion = None # on réinitialise l'évènement jusqu'à la prochaine fois qu'il sera touché

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
        texte = self.score_font.render("VICTOIRE !", 1, (255,255,255))
        r = texte.get_rect()
        r.x = window_longueur/2 - r.centerx
        r.y = window_largeur/2 - r.centery
        screen.blit(texte, r)
        
    def __defaite(self):
        """
        Affiche un écran de défaite et ferme le jeu
        """
        texte = self.score_font.render("DEFAITE", 1, (255, 0, 0))
        r = texte.get_rect()
        r.x = window_longueur / 2 - r.centerx
        r.y = window_largeur / 2 - r.centery
        screen.blit(texte, r)
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause de 3 secondes avant de quitter
        pygame.quit()# ferme le jeux




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
