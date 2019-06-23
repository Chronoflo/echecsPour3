import Pieces

class Plateau(list):
    def __init__(self, listeJoueurs):
        super().__init__(initialisation_plateau(listeJoueurs))

    def sur_sélection_pièce(self, coordonnées):
        p, d, g = coordonnées
        depAVerifier, depAVerifierEnnemis = Pieces.traduction_en_couples_déplacements(
            *self[p][d][g].deplacementsPossibles(), coordonnées)
        depVerifies = []
        for dep in depAVerifier:
            depVerifies.append(dep)

    def sur_déplacement_validé(self, coordonnéesPion, coordonnéesCible):
        p1,d1,g1, p2,d2,g2 = *coordonnéesPion, *coordonnéesCible
        if self[p2][d2][g2] is not None:
            pionEnnemi: Pieces.Piece = self[p2][d2][g2]
            pionEnnemi.joueur.piecesRestantes.remove(pionEnnemi)
        self[p1][d1][g1], self[p2][d2][g2] = None, self[p1][d1][g1]


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