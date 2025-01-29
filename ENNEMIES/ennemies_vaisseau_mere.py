import pygame
from os import path, getcwd

from types_perso import Coordonnees
from information_jeu import tire_ennemie
from TIRES.tire import Tire



"""
Fichier .py permettant de contrôler tous les ennemies présent sur l'écran.

Contient :

    1 class : Ennemie
"""
ennemie_mort = pygame.image.load(path.join(getcwd(), "ENNEMIES\Assets\space__0009_EnemyExplosion.png"))

class Ennemie:

    def __init__(self, screen: pygame.Surface, x: Coordonnees, y: Coordonnees, ennemie_anim: tuple[str, str]):
        """
        Initialisation d'un ennemie
        :param screen: la surface ou dessiner
        """

        self.__screen: pygame.Surface = screen

        self.__rect = pygame.Rect(x, y, 25, 25)

        self.__vie: bool = True # si l'ennemeie est en vie ou non

        self.__ennemie_anim: tuple[pygame.Surface, pygame.Surface] = (pygame.image.load(path.join(getcwd(), f"ENNEMIES\Assets\{ennemie_anim[0]}")), pygame.image.load(path.join(getcwd(), f"ENNEMIES\Assets\{ennemie_anim[1]}")))
        self.__current_anim: int = 0


    def afficher_ennemie(self) -> None:
        """
        affiche l'ennemie à sa position x,y
        :return: None
        """
        if self.__vie:
            #pygame.draw.rect(surface=self.__screen,
                               #color=(70, 58, 255),
                               #rect=self.__rect)

            self.__screen.blit(self.__ennemie_anim[self.__current_anim], self.__rect)

    def tuer(self) -> None:
        """
        Tue l'ennemie
        :return:
        """
        new_rect = pygame.Rect(self.__rect.x, self.__rect.y, 26, 16)
        self.__screen.blit(ennemie_mort, self.__rect)
        self.__vie = False


    def tirer(self):
        """
        L'ennemie tire
        :return:
        """
        largeur_tire = 2
        return Tire(self.__screen, x=self.__rect.center[0] - largeur_tire//2, y=self.__rect.y, longueur_tire=10, direction_tire=10, color=(255, 0, 0), appartient_a=tire_ennemie, largeur_tire=largeur_tire)

    @property
    def x(self) -> Coordonnees:
        """
        Retourne la coordonnée X de l'ennemie
        :return: une coordonnée X
        """
        return self.__rect.x

    @x.setter
    def x(self, définir_x: Coordonnees):
        """
        définit une valeur à X
        :param ajouter_a_x: le nombre à ajouter à la coordonnée X
        :return: None
        """
        self.__rect.x = définir_x
        self.__current_anim = 1 - self.__current_anim # change l'annimation du personnage

    @property
    def y(self) -> Coordonnees:
        """
        Retourne la coordonnée Y de l'ennemie
        :return: une coordonnée Y
        """
        return self.rect.y

    @y.setter
    def y(self, définir_y: Coordonnees):
        """
        définit une valeur à Y
        :param ajouter_a_y: le nombre à ajouter à la coordonnée Y
        :return: None
        """
        self.__rect.y = définir_y

    @property
    def vie(self) -> bool:
        """
        Renvoie si l'ennemie est envie ou non
        :return: True -> en vie     False -> mort
        """
        return self.__vie

    @property
    def tire(self) -> str:
        """
        Renvoie à qui appartien le tire
        :return:
        """
        return tire_ennemie

    @property
    def rect(self) -> pygame.Rect:
        """
        Renvoie le rectangle de l'ennemie
        :return:
        """
        return self.__rect
