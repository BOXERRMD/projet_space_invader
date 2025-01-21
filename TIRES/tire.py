from __future__ import annotations
import pygame

from types_perso import Coordonnees

from typing import Union, TypeVar, TYPE_CHECKING

if TYPE_CHECKING: # permet une importation non circulaire des modules mais uniquement sous la forme d'un type !!!
    from VAISSEAU.vaisseau_mere import Vaisseau
    from ENNEMIES.ennemies_vaisseau_mere import Ennemie

    type_vaisseau = Vaisseau
    Tire_appartenance = TypeVar("Tire_appartenance", type(Vaisseau), type(Ennemie), None)

"""
Comporte une class permettant de gérer les tires des ennemies et celui du joueurs.
"""


class Tire:

    def __init__(self, screen: pygame.Surface, x: Coordonnees, y: Coordonnees, longueur_tire: int, direction_tire: Coordonnees, color: tuple[int, int, int], appartient_a: Tire_appartenance = None, largeur_tire: int = 1):
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
        self.__color: tuple[int] = color
        self.__rect: pygame.Rect = pygame.Rect(x, y, longueur_tire, largeur_tire)

        self.__appartien_a: Tire_appartenance = appartient_a # à qui appartient le tire (sera le type de la class à qui le tire appartient)

    def afficher_tire(self, vaisseau_mere: Vaisseau, ennemies: list[Ennemie]) -> bool:
        """
        Affiche le tir à l'écran
        :param vaisseau_mere: Le vaiseau mère actuellement en jeu
        :param ennemies: La liste des ennemies en jeu
        :return: True si le tire a touché, False sinon
        """
        if self.__collision(vaisseau_mere):
            return True

        for ennemie in ennemies:
            if self.__collision(ennemie):
                return True

        pygame.draw.rect(self.__screen, color=self.__color, rect=self.__rect)
        return False

    def __collision(self, objet: Union[Vaisseau, Ennemie]) -> bool:
        """
        gère la collision des objets avec le tire en cours
        :param objet: l'objet d'ou il faut vérifier la collision
        :return: Renvoie True si le tir à toucher sa cible
        """
        if self.__rect.colliderect(objet.rect):  # si les rectangles se chevauche
            if isinstance(objet, Vaisseau): # BLOCAGE CAR LE TYPE N'EST PAS RECONNU = CHANGER LA MANI7RE DE RECONNAITRE LES TIRES (par des str par exemple)
                objet.vie -= 1
                return True

            elif isinstance(objet, Ennemie):
                objet.tuer()
                return True

            else:
                return False



    @property
    def start_coordonnees(self) -> tuple[Coordonnees, Coordonnees]:
        """
        Renvoie un tuple de coordonnées du départ du trait
        :return:
        """
        return self.__start_pose

    @property
    def end_coordonnees(self) -> tuple[Coordonnees, Coordonnees]:
        """
        Renvoie un tuple de coordonnées de la fin du trait
        :return:
        """
        return self.__end_pose
