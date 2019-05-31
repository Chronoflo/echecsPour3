from Pieces import *

class Joueur:
    def __init__(self, nomJoueur, couleur):
        self.pseudo = nomJoueur
        self.couleur = couleur

        self.roi = Roi(nomJoueur)
        self.reine = Reine(nomJoueur)
        self.fou1 = Fou(nomJoueur)
        self.fou2 = Fou(nomJoueur)
        self.tour1 = Tour(nomJoueur)
        self.tour2 = Tour(nomJoueur)
        self.cavalier1 = Cavalier(nomJoueur)
        self.cavalier2 = Cavalier(nomJoueur)
        self.pion1 = Pion(nomJoueur)
        self.pion2 = Pion(nomJoueur)
        self.pion3 = Pion(nomJoueur)
        self.pion4 = Pion(nomJoueur)
        self.pion5 = Pion(nomJoueur)
        self.pion6 = Pion(nomJoueur)
        self.pion7 = Pion(nomJoueur)
        self.chevre = Chevre(nomJoueur)