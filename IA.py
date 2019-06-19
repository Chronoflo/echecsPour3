import Pieces
import joueur
import copy

ptsVert = 110
ptsRouge = 110
ptsBleu = 110


def initialise_var():
    global ptsVert
    global ptsRouge
    global ptsBleu
    ptsVert = 110
    ptsRouge = 110
    ptsBleu = 110



def coup_à_jouer(player, plateau):
    """Entrées : player, plateau
    Précondition : c’est à player de jouer
    Sorties : le prochain coup joué par player"""
    coupsPossible = coups_possible(posPlateau, plateau)
    aJouer = coupsPossible[0]
    scoreEssai = score(player, jouer(aJouer, plateau), profondeur)
    pieceChoisie = 0
    for i, coup in enumerate(coupsPossible) :
    	scoreTest = score(player, jouer(coup, plateau), profondeur)
    	if scoreTest > scoreEssai :
            scoreEssai = scoreTest
            aJouer = coup
            pieceChoisie = i

    return pieceChoisie, aJouer



def score(player, plateau, profondeur):
    """Entrées : player,plateau,profondeur
    Sorties : un entier d’autant plus grand que player a de chances de gagner"""

    if profondeur!=0 and not(partie_finie) :
    	coup = prochainCoup(joueur.joueur_suivant(player), plateau)

    return score(joueur.joueur_suivant(player), jouer(coup,plateau), profondeur-1)


def jouer(coup,plateau):
    truc



def coups_possible(posPlateau, plateau):
    """ fonction qui crée la tableau de tous les déplacements possibles
    de toutes les pieces possibles appartenant à l'IA"""
    coupPossibles=[]
    for position in posPlateau:
        p, d, g = posPlateau
        piece = plateau[p][d][g]
        deplacements = Pieces.dep_effectifs(Pieces.traduction_en_couples_déplacements(*piece.deplacements_possibles(None), position))
        coupPossibles.append((deplacements))

    return coupPossibles



def trouve_pieces_joueur(player, plateau):
    tabPieces=[]
    for p in range(3):
        for x in range(6):
            for y in range(6):
                if joueur.plateau[p][x][y] == player:
                    tabPieces.append((p,x,y))

    return tabPieces



def jeu_IA(plateau, difficulté, IA):
    """fonction principale qui s'occupe de faire jouer l'IA
    Entrée : le plateau qui contient l'etat du jeu,
             la difficulté qui détermine le niveau de l'IA c'est à dire combien de tours a l'avance prévoit l'IA
    Précondition : c'est à l'IA de jouer
    Sortie : déplacement de la piece par l'IA"""

    nouvPlat = copy.deepcopy(plateau) # utilise un autre plateau pour les tests

    profondeur = 3*difficulté

    tabPosPieces = trouve_pieces_joueur(IA ,nouvPlat)
    coupsPossible =  coup_possible(tabPosPieces, nouvPlat)
    numPiece, coupJoué = coup_à_jouer(IA, nouvPlat)
    pieceJoué = tabPosPieces[numPiece]
    return pieceJoué, coupJoué