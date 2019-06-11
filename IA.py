# Les 2 programmes suivant sont ceux du prof

def coup_à_jouer(joueur, plateau):
    """Entrées : joueur, etatJeu
    Précondition : c’est à joueur de jouer
    Sorties : le prochain coup joué par joueur"""
    m = 0
    aJouer = coupPossible(Roi)
    for c in coupsPossibles :
    	essai = score(joueur, jouer(c, etatJeu), profondeur)
    	if essai > m :
    		m = essai
    		aJouer = c

    return aJouer

def score(joueur, jouer, profondeur):
    """Entrées : joueur,etatJeu,profondeur
    précondition : c’est à l’adversaire de joueur de jouer
    Sorties : un entier d’autant plus grand que joueur a de chances de gagner"""

    if profondeur==0 or partie_finie :
        None
    else:
        #changer autre(joueur) car il y a 3 joueurs
    	c = prochainCoup(autre(joueur), etatJeu)
    	return score(autre(joueur), joueur(c,etatJeu), profondeur-1)

