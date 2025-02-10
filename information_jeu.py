"""
Les informations du jeu.
"""

# jeu
FPS: int = 60

# fenêtre du jeu
window_longueur: int = 640
window_largeur: int = 480

# vaisseau mère
vaisseau_posX: float = window_longueur/2
vaisseau_posY: float = window_largeur - 30

vaisseau_vitesse: int = 10
tire_vaisseau: str = "vaisseau"


# ennemies

rayon_ennemie: int = 14

colonnes: int = 1
espacement_collone: float = window_longueur / colonnes

lignes: int = 5
espacement_ligne: int = rayon_ennemie*2 + 10
tire_ennemie: str = "ennemie"