# Les 2 programmes suivant sont ceux du prof

import Pieces

ptsVert = 0
ptsRouge = 0
ptsBleu = 0

def initialise_var():
    global ptsVert
    global ptsRouge
    global ptsBleu
    ptsVert = 0
    ptsRouge = 0
    ptsBleu = 0


def coup_à_jouer(joueur, plateau):
    """Entrées : joueur, etatJeu
    Précondition : c’est à joueur de jouer
    Sorties : le prochain coup joué par joueur"""
    m = 0
    aJouer = coupPossible(truc)
    for c in coupsPossibles :
    	essai = score(joueur, jouer(c, etatJeu), profondeur)
    	if essai > m :
    		m = essai
    		aJouer = c

    return aJouer

import joueur

def score(player, jouer, profondeur):
    """Entrées : player,etatJeu,profondeur
    précondition : c’est à l’adversaire de player de jouer
    Sorties : un entier d’autant plus grand que player a de chances de gagner"""

    if profondeur!=0 and not(partie_finie) :
        #changer autre(player) car il y a 3 joueurs
    	c = prochainCoup(joueur.joueur_suivant(player), etatJeu)

    return score(autre(player), player(c,etatJeu), profondeur-1)



def coup_possibles(posPlateau, plateau):
    """ fonction qui crée la tableau de tous les déplacements possibles
    de toutes les pieces possibles appartenant à l'IA"""
    #a gerer : cas ou la foncion renvois un couple
    coupPossibles=[]
    for position in posPlateau:
        i, j, k = posPlateau
        piece = plateau[i][j][k]
        deplacements = Pieces.dep_effectifs(Pieces.traduction_en_couples_déplacements(*piece.deplacements_possibles(None), position))
        coupPossibles.append((deplacements))

    return coupPossibles