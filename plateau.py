class Plateau(list):
    def __init__(self, listeJoueurs):
        super().__init__(initialisation_plateau(listeJoueurs))


def initialisation_plateau(listeJoueurs):
    """ Retourne un plateau pour len(listeJoueurs) joueurs. """
    return [
        [
            [joueur.roi,   joueur.tour2,     joueur. fou2,     joueur.pion7, None, None],
            [joueur.fou1,  joueur.reine,     joueur.cavalier2, joueur.pion6, None, None],
            [joueur.tour1, joueur.cavalier1, joueur.chevre,    joueur.pion5, None, None],
            [joueur.pion1, joueur.pion2,     joueur.pion3,     joueur.pion4, None, None],
            [None,         None,             None,             None,         None, None],
            [None,         None,             None,             None,         None, None]
        ]
        for joueur in listeJoueurs]


from joueur import *


joueurs = [Joueur("Arhur", 2), Joueur("Sarah", 3), Joueur("Florian", 4)]

plateau = Plateau(joueurs)
print(plateau[0][0][0].nomJoueur)