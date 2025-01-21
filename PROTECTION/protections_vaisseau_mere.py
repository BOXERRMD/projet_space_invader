import pygame


"""
Fichier .py permettant de contrôler toutes les protections présent sur l'écran.

Contient :

    1 class : Protection
"""

class Protection:

    def __init__(self, screen: pygame.Surface):
        """
        Initialisation d'une protection du vaisseau mère
        :param screen: la surface ou dessiner
        """

        self.__screen: pygame.Surface = screen