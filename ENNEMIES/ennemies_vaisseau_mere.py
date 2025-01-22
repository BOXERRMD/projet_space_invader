import pygame

from types_perso import Coordonnees
from information_jeu import tire_ennemie



"""
Fichier .py permettant de contrôler tous les ennemies présent sur l'écran.

Contient :

    1 class : Ennemie
"""

class Ennemie:

    def __init__(self, screen: pygame.Surface, x: Coordonnees, y: Coordonnees, radius: int):
        """
        Initialisation d'un ennemie
        :param screen: la surface ou dessiner
        """

        self.__screen: pygame.Surface = screen

        self.__x: Coordonnees = x
        self.__y: Coordonnees = y

        self.__radius = radius # le rayon de la shère

        self.__vie: bool = True # si l'ennemeie est en vie ou non


    def afficher_ennemie(self) -> None:
        """
        affiche l'ennemie à sa position x,y
        :return: None
        """
        if self.__vie:
            pygame.draw.circle(surface=self.__screen,
                               color=(70, 58, 255),
                               radius=self.__radius,
                               center=(self.__x, self.__y))

    def tuer(self) -> None:
        """
        Tue l'ennemie
        :return:
        """
        self.__vie = False

    def tirer(self):
        """
        L'ennemie tire
        :return:
        """
        pass

    @property
    def x(self) -> Coordonnees:
        """
        Retourne la coordonnée X de l'ennemie
        :return: une coordonnée X
        """
        return self.__x

    @x.setter
    def x(self, définir_x: Coordonnees):
        """
        définit une valeur à X
        :param ajouter_a_x: le nombre à ajouter à la coordonnée X
        :return: None
        """
        self.__x = définir_x

    @property
    def y(self) -> Coordonnees:
        """
        Retourne la coordonnée Y de l'ennemie
        :return: une coordonnée Y
        """
        return self.__y

    @y.setter
    def y(self, définir_y: Coordonnees):
        """
        définit une valeur à Y
        :param ajouter_a_y: le nombre à ajouter à la coordonnée Y
        :return: None
        """
        self.__x = définir_y

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
