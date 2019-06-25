import Pieces


class Joueur:
    """ Classe répresentant un joueur. Un joueur possède un nom, une couleur et ses pions. """
    def __init__(self, nomJoueur, terrainDOrigine, couleur):
        """ Crée un joueur."""
        self.nom = nomJoueur
        self.couleur = couleur
        self.score = 110
        self.terrainDOrigine = terrainDOrigine

        self.roi = Pieces.Roi(self, terrainDOrigine)
        self.reine = Pieces.Reine(self, terrainDOrigine)
        self.fou1 = Pieces.Fou(self, terrainDOrigine)
        self.fou2 = Pieces.Fou(self, terrainDOrigine)
        self.tour1 = Pieces.Tour(self, terrainDOrigine)
        self.tour2 = Pieces.Tour(self, terrainDOrigine)
        self.cavalier1 = Pieces.Cavalier(self, terrainDOrigine)
        self.cavalier2 = Pieces.Cavalier(self, terrainDOrigine)
        self.pion1 = Pieces.Pion(self, terrainDOrigine)
        self.pion2 = Pieces.Pion(self, terrainDOrigine)
        self.pion3 = Pieces.Pion(self, terrainDOrigine)
        self.pion4 = Pieces.Pion(self, terrainDOrigine)
        self.pion5 = Pieces.Pion(self, terrainDOrigine)
        self.pion6 = Pieces.Pion(self, terrainDOrigine)
        self.pion7 = Pieces.Pion(self, terrainDOrigine)
        self.chat = Pieces.Chat(self, terrainDOrigine)

        self.piecesRestantes = [self.roi, self.reine, self.fou1, self.fou2, self.tour1, self.tour2,
                                self.cavalier1, self.cavalier2, self.pion1, self.pion2, self.pion3,
                                self.pion4, self.pion5, self.pion6, self.pion7, self.chat]

    def __str__(self):
        return self.nom


class IA(Joueur):
    """C'est l'IA, donc n'est pas contrôlée par les joueurs"""
    nomIA = ["AlphaPasGo", "DownTech", "DeepOrange"]
    numIA = 0

    def __init__(self, terrainDOrigine, couleur, difficulté):
        super(IA, self).__init__(IA.nomIA[IA.numIA], terrainDOrigine, couleur)
        IA.numIA += 1
        self.difficulté = difficulté


class ListeDeJoueurs(list):
    """ Une liste de joueurs. """
    def __init__(self, *joueurs, copie_de=None):
        if copie_de is None:
            super(ListeDeJoueurs, self).__init__(joueurs)
            self.iJoueurActuel = 0
        else:
            # Crée une copie de copie_de
            super(ListeDeJoueurs, self).__init__([Joueur(joueur.nom, joueur.terrainDOrigine, joueur.couleur) for joueur in copie_de])
            self.iJoueurActuel = copie_de.iJoueurActuel

    def __str__(self):
        return str([joueur.nom for joueur in self])

    def joueur_suivant(self):
        if self.iJoueurActuel + 1 < len(self):
            self.iJoueurActuel += 1
        else:
            self.iJoueurActuel = 0

        return self[self.iJoueurActuel]

    def joueur_actuel(self):
        return self[self.iJoueurActuel]

    def enleve_joueur(self, joueur):
        try:
            iJoueurAEnlever = self.index(joueur)
        except ValueError:
            print("Ce joueur ne joue pas.")
            return None
        else:
            if iJoueurAEnlever <= self.iJoueurActuel:
                self.iJoueurActuel -= 1
            del self[iJoueurAEnlever]


if __name__ == '__main__':
    listeJoueurs = ListeDeJoueurs("Arthur", "Florian", "Sarah")
    listeJoueurs.joueur_suivant()
    listeJoueurs.enleve_joueur("Florian")
    listeJoueurs.joueur_suivant()
    listeJoueurs.joueur_suivant()
    print(listeJoueurs.joueur_actuel())
    listeJoueurs.joueur_suivant()
