
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
        self.__x: Coordonnees = x
        self.__y: Coordonnees = y

        self.__longueur: int = 25
        self.__largeur: int = 25

        self.__screen: pygame.Surface = screen
        
        self.__vie: int = 1 # sa vie avant de mourir
        
        
    def est_en_vie(self) -> bool:
        return self.__vie <= 0

    def afficher_vaisseau(self) -> None:
        """
        Affiche le vaisseau à sa position x y
        :return: None
        """
        pygame.draw.rect(self.__screen, 'white', rect=(self.__x, self.__y, self.__longueur, self.__largeur))

    def tirer(self) -> Tire:
        """
        Tire un laser au dessus du vaisseau
        :return: Un tire appartanant au vaisseau
        """
        return Tire(self.__screen, x=self.__x+self.__longueur/2, y=self.__y, longueur_tire=10, direction_tire=-10, color=(125, 20, 99), appartient_a=Vaisseau)

    @property
    def vitesse(self) -> int:
        """
        Renvoie la vitesse du vaisseau
        :return: la vitesse du vaisseau mère
        """
        return self.__x

    @vitesse.setter
    def vitesse(self, new_vitesse: int) -> None:
        """
        Met new_vitesse à la vitesse du vaisseau mère
        :param new_vitesse: la vitesse du vaisseau mère
        :return: None
        """
        if self.__x + new_vitesse + self.__longueur > window_longueur or self.__x + new_vitesse < 0:
            return

        self.__x += new_vitesse

    @property
    def x(self) -> Coordonnees:
        """
        Renvoie la coordonnée X du vaisseau
        :return:
        """
        return self.__x

    @property
    def y(self) -> Coordonnees:
        """
        Renvoie la coordonnée Y du vaisseau
        :return:
        """
        return self.__y

    @property
    def longueur(self) -> int:
        """
        Renvoie la longueur du vaisseau
        :return:
        """
        return self.__longueur

    @property
    def largeur(self) -> int:
        """
        Renvoie la largeur du vaisseau
        :return:
        """
        return self.__largeur

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
