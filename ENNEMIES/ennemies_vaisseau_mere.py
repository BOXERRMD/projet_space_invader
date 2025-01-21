import pygame



"""
Fichier .py permettant de contrôler tous les ennemies présent sur l'écran.

Contient :

    1 class : Ennemie
"""

class Ennemie:

    def __init__(self, screen: pygame.Surface):
        """
        Initialisation d'un ennemie
        :param screen: la surface ou dessiner
        """

        self.__screen: pygame.Surface = screen