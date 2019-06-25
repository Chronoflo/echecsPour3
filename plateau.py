from Pieces import Piece, Tour, Pion, Reine, promotion_reine, Roi
from joueur import ListeDeJoueurs


class Plateau(list):
    def __init__(self, listeJoueurs: ListeDeJoueurs):
        super().__init__(initialisation_plateau(listeJoueurs))
        self.listeJoueurs = listeJoueurs

    def sur_sélection_pièce(self, coordonnées):
        pass

    def case(self, coords):
        p, d, g = coords
        return self[p][d][g]

    def sur_déplacement_validé(self, coordonnéesPion, coordonnéesCible):
        p1,d1,g1, p2,d2,g2 = *coordonnéesPion, *coordonnéesCible
        piece = self[p1][d1][g1]
        remplacement = None

        if self[p2][d2][g2] is not None:
            cible: Piece = self[p2][d2][g2]

            if isinstance(cible, Tour) and piece.joueur.nom == cible.joueur.nom:
                # Rocks
                if cible is piece.joueur.tour1:
                    self[p1][1][0] = cible
                else:
                    remplacement = cible
                cible.emplacementInitial = False
            else:
                # mange pièce
                cible.joueur.piecesRestantes.remove(cible)
                # échec et mat
                if isinstance(cible, Roi):
                    cible.joueur.enVie = False
                    self.listeJoueurs.enleve_joueur(cible.joueur)

        # Promotion des pions
        if isinstance(piece, Pion):
            diff_terrain = (p2 - piece.terrainOrigine) % 3
            if diff_terrain == 1 and d2 == 0 or diff_terrain == 2 and g2 == 0:
                piece = promotion_reine(piece)

        piece.emplacementInitial = False
        piece.terrainActuel = p2
        self[p1][d1][g1], self[p2][d2][g2] = remplacement, piece


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
        for joueur in listeJoueurs]
