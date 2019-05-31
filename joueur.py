from Pieces import *

class Joueur:
    """ Classe répresentant un joueur. Un joueur possède un nom, une couleur et ses pions. """
    def __init__(self, nomJoueur, couleur):
        """ Crée un joueur."""
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

        self.piecesRestantes = [self.roi, self.reine, self.fou1, self.fou2, self.tour1, self.tour2,
                                self.cavalier1, self.cavalier2, self.pion1, self.pion2, self.pion3,
                                self.pion4, self.pion5, self.pion6, self.pion7, self.chevre]


class ListesDeJoueur:
    def __init__(self, *joueurs):
        self.joueurs = list(joueurs)
        self.iJoueurActuel = 0

    def joueur_suivant(self):
        if self.iJoueurActuel + 1 < len(self.joueurs):
            self.iJoueurActuel += 1
        else:
            self.iJoueurActuel = 0

        return self.joueurs[self.iJoueurActuel]

    def enleve_joueur(self, joueur):
        try:
            iJoueurAEnlever = self.joueurs.index(joueur)
        except ValueError:
            print("Ce joueur ne joue pas.")
            return None
        else:
            if iJoueurAEnlever <= self.iJoueurActuel:
                self.iJoueurActuel -= 1
            del self.joueurs[iJoueurAEnlever]