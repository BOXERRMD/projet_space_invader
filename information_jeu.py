"""
Les informations du jeu.
"""

# jeu
FPS: int = 25

# fenêtre du jeu
window_longueur: int = 640
window_largeur: int = 480

# vaisseau mère
vaisseau_posX: float = window_longueur/2
vaisseau_posY: float = window_largeur - 30


# ennemies

rayon_ennemie: int = 10

colonnes: int = 10
espacement_collone: float = window_longueur / rayon_ennemie

lignes: int = 5
espacement_ligne: int = 40