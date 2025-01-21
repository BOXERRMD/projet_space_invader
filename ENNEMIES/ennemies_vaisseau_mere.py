import pygame

from types_perso import Coordonnees



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
        self.__radius = radius


    def afficher_ennemie(self) -> None:
        """
        affiche l'ennemie à sa position x,y
        :return: None
        """
        pygame.draw.circle(surface=self.__screen, color=(70, 58, 255), radius=self.__radius, center=(self.__x, self.__y))


    @property
    def x(self) -> Coordonnees:
        """
        Retourne la coordonnée X de l'ennemie
        :return: une coordonnée X
        """
        return self.__x

    @x.setter
    def x(self, ajouter_a_x: Coordonnees):
        """
        Ajoute une valeur à X
        :param ajouter_a_x: le nombre à ajouter à la coordonnée X
        :return: None
        """
        self.__x += ajouter_a_x

    @property
    def y(self) -> Coordonnees:
        """
        Retourne la coordonnée Y de l'ennemie
        :return: une coordonnée Y
        """
        return self.__y

    @y.setter
    def y(self, ajouter_a_y: Coordonnees):
        """
        Ajoute une valeur à Y
        :param ajouter_a_y: le nombre à ajouter à la coordonnée Y
        :return: None
        """
        self.__x += ajouter_a_y