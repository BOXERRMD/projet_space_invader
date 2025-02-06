import pygame

class Protection:
    def __init__(self, screen: pygame.Surface, x: int, y: int):
        """
        Initialisation d'une protection du vaisseau mère
        :param screen: la surface où dessiner
        :param x: position X de la protection
        :param y: position Y de la protection
        """
        self.__screen: pygame.Surface = screen
        self.__rect = pygame.Rect(x, y, 50, 25)  # Largeur 100, hauteur 25
        self.__vie = 10  # 10 points de vie

    def afficher_protection(self) -> None:
        """
        Affiche la protection avec une couleur dépendant de la vie restante.
        """
        if self.__vie > 0:
            # Calcul de la couleur en fonction de la vie (du vert au rouge)
            vert = int((self.__vie / 10) * 255)
            rouge = 255 - vert
            couleur = (rouge, vert, 0)
            pygame.draw.rect(self.__screen, couleur, self.__rect)

    def degats(self) -> None:
        """
        Réduit la vie de la protection.
        """
        if self.__vie > 0:
            self.__vie -= 1

    @property
    def vie(self) -> bool:
        """
        Indique si la protection est encore en vie.
        """
        return self.__vie > 0

    @property
    def rect(self) -> pygame.Rect:
        """
        Retourne le rectangle de la protection pour les collisions.
        """
        return self.__rect

    @classmethod
    def creer_protections(cls, screen: pygame.Surface, nb_protections: int, y_position: int) -> list:
        """
        Crée une liste de protections réparties équitablement sur l'écran.
        :param screen: surface où dessiner les protections
        :param nb_protections: nombre total de protections à créer
        :param y_position: position Y des protections
        :return: liste d'instances de Protection
        """
        protections = []
        spacing = screen.get_width() // (nb_protections + 1)
        for i in range(nb_protections):
            x_position = spacing * (i + 1) - 50  # Centrage des protections
            protections.append(cls(screen, x_position, y_position))
        return protections
