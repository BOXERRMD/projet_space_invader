from __future__ import annotations
import pygame

from information_jeu import tire_vaisseau, tire_ennemie, window_largeur
from types_perso import Coordonnees

from typing import Union, TYPE_CHECKING

if TYPE_CHECKING: # permet une importation non circulaire des modules mais uniquement sous la forme d'un type !!!
    from VAISSEAU.vaisseau_mere import Vaisseau
    from ENNEMIES.ennemies_vaisseau_mere import Ennemie


"""
Comporte une class permettant de gérer les tires des ennemies et celui du joueurs.
"""


class Tire:

    def __init__(self, screen: pygame.Surface, x: Coordonnees, y: Coordonnees, longueur_tire: int, direction_tire: Coordonnees, color: tuple[int, int, int], appartient_a: Union[tire_vaisseau, tire_ennemie] = None, largeur_tire: int = 1):
        """
        Initialise un tire
        :param screen: la surface ou dessiner
        :param start_pose: Le départ du rectangle, un tuple de coordonnées x y
        :param direction_tire: la direction du tire (coordonnée y qui sera modifier en lui ajoutant cette valeur)
        :param color: La couleur du tire
        :param largeur_tire: L'épaisseur du tire (défaut 1)
        :param appartient_a: Permet de savoir à qui le tire appartient. Si None, le tire est neutre et fera des dégats à tous le monde.
        """

        self.__screen: pygame.Surface = screen
        self.__color: tuple[int, int, int] = color
        self.__rect: pygame.Rect = pygame.Rect(x, y, largeur_tire, longueur_tire)
        self.__direction_tire: Coordonnees = direction_tire

        self.__appartien_a: Union[tire_ennemie, tire_vaisseau] = appartient_a # à qui appartient le tire (sera le type de la class à qui le tire appartient)

    def afficher_tire(self):
        """
        Affiche le tir à l'écran
        :param vaisseau_mere: Le vaiseau mère actuellement en jeu
        :param ennemies: La liste des ennemies en jeu
        :return:
        """

        pygame.draw.rect(self.__screen, color=self.__color, rect=self.__rect)


    def collision(self, objet: Union[Vaisseau, Ennemie]) -> bool:
        """
        gère la collision des objets avec le tire en cours
        :param objet: l'objet d'ou il faut vérifier la collision
        :return: Renvoie True si le tir à toucher sa cible
        """
        if self.__rect.colliderect(objet.rect):  # si les rectangles se chevauche
            if objet.tire == tire_vaisseau: ##Tir vers le Vaisseau mère
                objet.vie -= 1
                return True

            elif objet.tire == tire_ennemie: ##Tir vers l'ennemi
                objet.tuer()
                return True

            else:
                return False

        if self.y < 0:  # si le tire sort de la limite du jeu côté ennemie
            return True

        elif self.y > window_largeur: # si le tire sort de la limite du jeu côté joueur
            return False



    @property
    def y(self) -> Coordonnees:
        """
        Renvoie la coordonnée Y du tire
        :return:
        """
        return self.__rect.y

    @y.setter
    def y(self, nouvelle_coordonnee_Y: Coordonnees):
        """
        Met une nouvelle coordonnée à Y
        :param nouvelle_coordonnee_Y: la nouvelle coordonnée qui remplace celle existante
        :return:
        """
        self.__rect.y = nouvelle_coordonnee_Y
