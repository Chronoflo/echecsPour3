from Pieces import Piece, Tour

class Plateau(list):
    def __init__(self, listeJoueurs):
        super().__init__(initialisation_plateau(listeJoueurs))

    def sur_sélection_pièce(self, coordonnées):
        pass

    def sur_déplacement_validé(self, coordonnéesPion, coordonnéesCible):
        p1,d1,g1, p2,d2,g2 = *coordonnéesPion, *coordonnéesCible
        piece = self[p1][d1][g1]
        remplacement = None

        if self[p2][d2][g2] is not None:
            cible: Piece = self[p2][d2][g2]
            if isinstance(cible, Tour) and piece.joueur.nom == cible.joueur.nom:
                remplacement = cible
                cible.emplacementInitial = False
            else:
                cible.joueur.piecesRestantes.remove(cible)

        piece.emplacementInitial = False
        piece.terrainActuel = p2
        self[p1][d1][g1], self[p2][d2][g2] = remplacement, self[p1][d1][g1]


def initialisation_plateau(listeJoueurs):
    """ Retourne un plateau pour len(listeJoueurs) joueurs. """
    return [
        [
            [joueur.roi,   joueur.tour2,     joueur.fou2,     joueur.pion7, None, None],
            [joueur.fou1,  joueur.reine,     joueur.cavalier2, joueur.pion6, None, None],
            [joueur.tour1, joueur.cavalier1, joueur.chat,    joueur.pion5, None, None],
            [joueur.pion1, joueur.pion2,     joueur.pion3,     joueur.pion4, None, None],
            [None,         None,             None,             None,         None, None],
            [None,         None,             None,             None,         None, None]
        ]
        for joueur in listeJoueurs.joueurs]