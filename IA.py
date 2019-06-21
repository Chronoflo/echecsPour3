import Pieces
import joueur
import copy
from plateau import Plateau

def trouve_pieces_et_coups_joueur(player, plateau: Plateau):
    """fonction qui enregistre dans un tableau tous les déplacements possibles de l'IA"""
    piecesCoupPossibles=[]
    for p in range(3):
        for x in range(6):
            for y in range(6):
                if isinstance(plateau[p][x][y], Pieces.Piece) and plateau[p][x][y].joueur == player:
                    position = (p,x,y)
                    deplacements = Pieces.dep_effectifs(Pieces.traduction_en_couples_déplacements(*piece.deplacements_possibles(None), position))
                    piecesCoupPossibles.append((position, deplacements))

    return piecesCoupPossibles



def coup_à_jouer(player, plateau: Plateau, profondeur):
    """Entrées : player, plateau
    Précondition : c’est à player de jouer
    Sorties : le prochain coup joué par player"""
    nouvPlat = copy.deepcopy(plateau) # utilise un autre plateau pour les tests
    piecesCoupPossibles = trouve_pieces_et_coups_joueur(player, plateau)
    aJouer = piecesCoupPossibles[0]
    scoreJouer = score(player, jouer(aJouer, nouvPlat), profondeur)
    coordPieceChoisie = 0
    for i, coup in enumerate(piecesCoupPossibles[1:]) :
        nouvPlat = copy.deepcopy(plateau) # utilise un autre plateau pour les tests
        scoreTest = score(player, jouer(coup, nouvPlat), profondeur)
        if scoreTest > scoreJouer :
            scoreJouer = scoreTest
            aJouer = coup
            coordPieceChoisie = i

    return coordPieceChoisie, aJouer



def coup_immédiat(player, plateau: Plateau, profondeur, score):
    """Entrées : celui qui joue, plateau, niveau de l'IA
    Sorties : un entier d’autant plus grand que player a de chances de gagner"""

    if profondeur==0 or partie_finie :
        return score

    else:
        coup = coup_à_jouer(joueur.joueur_suivant(player), nouvPlat)

    return jouer(joueur.joueur_suivant(player), jouer(coup,nouvPlat), profondeur-1)



def jouer(player, coordPiece, nouvCase, plateau: Plateau):
    """joue un coup sur une copie du plateau et enregistre le score actuel
    Entrée : le coup a jouer c'est a dire la piece et la case sur laquelle elle va
    Sortie : le nouveau plateau (la copie qui a changée) , et le score des joueurs """
    p1, x1, y1 = coordPiece
    p2, x2, y2 = nouvCase

    if isinstance(plateau[p2][x2][y2], Pieces.Piece):
        pieceKill = plateau[p2][x2][y2]
        modif_score(player, coordPiece, nouvCase, plateau, True)

    else :
        plateau.sur_déplacement_validé(coordPiece, nouvCase)
        modif_score(player, coordPiece, nouvCase, plateau, False)

def modif_score(player, coordPiece, nouvCase, plateau, bool):
    p1, x1, y1 = coordPiece
    p2, x2, y2 = nouvCase

    differenceTerrain = abs(p1 - p2) % 3

    if differenceTerrain == 0:
        factTer = 1
    elif differenceTerrain == 1 and plateau[p1][x1][y1].terrainActuel == plateau[p1][x1][y1].terrainOrigine:


    if bool:
        truc_pour_modif_score_des_2_joueurs

    else :
        scoreSupp = truc
        player.score += scoreSupp


def jeu_IA(plateau: Plateau, difficulté, IA):
    """fonction principale qui s'occupe de faire jouer l'IA
    Entrée : le plateau qui contient l'etat du jeu,
             la difficulté qui détermine le niveau de l'IA c'est à dire combien de tours a l'avance prévoit l'IA
    Précondition : c'est à l'IA de jouer
    Sortie : déplacement de la piece par l'IA"""

    profondeur = 3*difficulté
    # profondeur = nombre de coups d'avance (compte les coups des 3 joueurs)
    # difficulté = nombre de tours de plateau d'avance (ne compte que les fois où l'IA joue)

    numPiece, coupJoué = coup_à_jouer(IA, plateau, profondeur)
    pieceJoué = tabPosPieces[numPiece]
    return pieceJoué, coupJoué