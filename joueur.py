import Pieces


class Joueur:
    """ Classe répresentant un joueur. Un joueur possède un nom, une couleur et ses pions. """
    def __init__(self, nomJoueur, terrainDOrigine, couleur):
        """ Crée un joueur."""
        self.pseudo = nomJoueur
        self.couleur = couleur
        self.score = 110

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




class IA(Joueur):
    """C'est l'IA, donc n'est pas contrôlée par les joueurs"""
    nomIA = ["AlphaPasGo", "DownTech", "DeepOrange"]
    numIA = 0
    def __init__(self, terrainDOrigine, couleur, difficulté):
        super(IA, self).__init__(IA.nomIA[IA.numIA], terrainDOrigine, couleur)
        IA.numIA +=1
        self.difficulté = difficulté

class ListeDeJoueurs:

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
