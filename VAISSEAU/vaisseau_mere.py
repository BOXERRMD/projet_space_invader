
import pygame
from types_perso import Coordonnees
from information_jeu import window_longueur

from TIRES.tire import Tire




"""
Fichier .py permettant de contrôler le vaisseau mère présent sur l'écran
Contient :

    1 class : Vaisseau
"""

class Vaisseau:

    def __init__(self, x: Coordonnees, y: Coordonnees, screen: pygame.Surface, vitesse: int = 5):
        """
        Initialisation du vaisseau mère
        :param x: la coordonnée x du vaisseau
        :param y: la coordonnée y du vaisseau
        :param vitesse: la vitesse du vaisseau
        :param screen: la surface ou dessiner
        """

        self.__rect = pygame.Rect(x, y, 25, 25)

        self.__screen: pygame.Surface = screen
        
        self.__vie: int = 1 # sa vie avant de mourir
        self.__vitesse: int = 0
        
        
    def est_en_vie(self) -> bool:
        return self.__vie <= 0

    def afficher_vaisseau(self) -> None:
        """
        Affiche le vaisseau à sa position x y
        :return: None
        """
        pygame.draw.rect(self.__screen, 'white', rect=self.__rect)

    def tirer(self) -> Tire:
        """
        Tire un laser au dessus du vaisseau
        :return: Un tire appartanant au vaisseau
        """
        return Tire(self.__screen, x=self.__rect.center[0], y=self.__rect.y, longueur_tire=10, direction_tire=-10, color=(125, 20, 99), appartient_a=Vaisseau)

    @property
    def vitesse(self) -> int:
        """
        Renvoie la vitesse du vaisseau
        :return: la vitesse du vaisseau mère
        """
        return self.__vitesse

    @vitesse.setter
    def vitesse(self, new_vitesse: int) -> None:
        """
        Met new_vitesse à la vitesse du vaisseau mère
        :param new_vitesse: la vitesse du vaisseau mère
        :return: None
        """
        if self.__rect.x + new_vitesse + self.__rect.width > window_longueur or self.__rect.x + new_vitesse < 0:
            return

        self.__rect.x += new_vitesse

    @property
    def x(self) -> Coordonnees:
        """
        Renvoie la coordonnée X du vaisseau
        :return:
        """
        return self.__rect.x

    @property
    def y(self) -> Coordonnees:
        """
        Renvoie la coordonnée Y du vaisseau
        :return:
        """
        return self.__rect.y

    @property
    def longueur(self) -> int:
        """
        Renvoie la longueur du vaisseau
        :return:
        """
        return self.__rect.width

    @property
    def largeur(self) -> int:
        """
        Renvoie la largeur du vaisseau
        :return:
        """
        return self.__rect.height

    @property
    def vie(self) -> int:
        """
        Renvoie le nombre de vie restant
        :return:
        """
        return self.__vie

    @vie.setter
    def vie(self, nouvelle_vie):
        """
        Met la vie du vaisseau à ...
        :param nouvelle_vie: la nouvelle vie du vaisseau
        :return:
        """
        self.__vie = nouvelle_vie

    @property
    def rect(self) -> pygame.Rect:
        """
        Revoie le rectangle du vaisseau
        :return:
        """
        return self.__rect
