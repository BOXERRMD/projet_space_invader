
import pygame
from os import path, getcwd
from types_perso import Coordonnees
from information_jeu import window_longueur, tire_vaisseau

from TIRES.tire import Tire # Et la, c'est le drâme... ## fait quelque chose en rapport avec les tirs




"""
Fichier .py permettant de contrôler le vaisseau mère présent sur l'écran
Contient :

    1 class : Vaisseau
"""
asset_vaisseau = pygame.image.load(path.join(getcwd(), "VAISSEAU\Assets\space__0006_Player.png"))
explosion = pygame.image.load(path.join(getcwd(), "VAISSEAU\Assets\space__0010_PlayerExplosion.png"))

class Vaisseau:

    def __init__(self, x: Coordonnees, y: Coordonnees, screen: pygame.Surface):
        """
        Initialisation du vaisseau mère
        :param x: la coordonnée x du vaisseau
        :param y: la coordonnée y du vaisseau
        :param vitesse: la vitesse du vaisseau
        :param screen: la surface ou dessiner
        """

        self.__rect = pygame.Rect(x, y, 26, 16) # dimension du rectangle de collision

        self.__screen: pygame.Surface = screen
        
        self.__vie: int = 3 # sa vie avant de mourir
        self.__vitesse: int = 0
        self.__touche = False
        
        
    def est_en_vie(self) -> bool:
        return self.__vie <= 0

    def afficher_vaisseau(self) -> None:
        """
        Affiche le vaisseau à sa position x y
        :return: None
        """
        if self.__touche == True:
            self.__screen.blit(explosion, self.__rect)

        else:
            self.__screen.blit(asset_vaisseau, self.__rect)

    def tirer(self) -> Tire:
        """
        Tire un laser au dessus du vaisseau
        :return: Un tire appartanant au vaisseau
        """
        largeur_tire = 3
        # personnellement, cette ligne est vraiment grande. MAIS elle rentre sur mon écran :D c'est vraiment une phrase typique du developpeur
        # qui n'a pas envie de corriger son code et qui dit "ça marche sur mon ordinateur :p"
        return Tire(self.__screen, x=self.__rect.center[0] - largeur_tire//2, y=self.__rect.y, longueur_tire=10, direction_tire=-10, color=(125, 20, 99), appartient_a=tire_vaisseau, largeur_tire=largeur_tire)

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

    @property
    def tire(self) -> str:
        """
        Renvoie à qui appartien le tire
        :return:
        """
        return tire_vaisseau

    @property
    def touche(self)->bool:
        """
        Renvoie si le vaisseau a été touché
        :return:
        """
        return self.__touche

    @touche.setter
    def touche(self, new: bool):
        """
        Modifie la valeur du vaisseau s'il a été touché
        Utiliser pour réinitialiser la valeur self.__touche à False après que le timer pour l'affichage du vaisseau explosé ait pris fin
        :param new:
        :return:
        """
        self.__touche = new
    
    def est_touche(self):
        """
        Si le vaisseau a été touché
        :return:
        """
        self.__touche = True
        
