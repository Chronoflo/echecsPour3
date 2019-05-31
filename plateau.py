class Plateau(list):
    def __init__(self, listeJoueurs):
        super().__init__(initialisation_plateau(listeJoueurs))


def initialisation_plateau(listeJoueurs):
    """ Retourne un plateau pour len(listeJoueurs) joueurs. """
    return [
        [
            [[joueur.Roi],   [joueur.Tour2],     [joueur. Fou2],     [joueur.Pion7], [None], [None]],
            [[joueur.Fou1],  [joueur.Reine],     [joueur.Cavalier2], [joueur.Pion6], [None], [None]],
            [[joueur.Tour1], [joueur.Cavalier1], [joueur.Chevre],    [joueur.Pion5], [None], [None]],
            [[joueur.Pion1], [joueur.Pion2],     [joueur.Pion3],     [joueur.Pion4], [None], [None]],
            [[None],         [None],             [None],             [None],         [None], [None]],
            [[None],         [None],             [None],             [None],         [None], [None]]
        ]
        for joueur in listeJoueurs]