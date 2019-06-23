import Pieces
import joueur
from copy import deepcopy
from plateau import Plateau


def trouve_pieces_et_coups_joueur(player, plateau: Plateau):
    """fonction qui enregistre dans un tableau tous les déplacements possibles de l'IA"""
    piecesCoupPossibles = []
    piecePossible = []
    for p in range(3):
        for x in range(6):
            for y in range(6):
                if isinstance(plateau[p][x][y], Pieces.Piece) and plateau[p][x][y].joueur == player:
                    position = (p,x,y)
                    deplacements = Pieces.dep_effectifs(Pieces.traduction_en_couples_déplacements(*piece.deplacements_possibles(None), position))
                    piecePossible.append(position)
                    piecesCoupPossibles.append(deplacements)

    return piecePossible, piecesCoupPossibles



def coup_à_jouer(player, plateau: Plateau, profondeur):
    """Entrées : player, plateau
    Precondition : c'est a player de jouer
    Sorties : le prochain coup joue par player"""
    nouvPlat = deepcopy(plateau) # utilise un autre plateau pour les tests
    piecesCoupPossibles = trouve_pieces_et_coups_joueur(player, plateau)
    aJouer = piecesCoupPossibles[0]
    scoreJouer = coup_immediat(player, jouer(aJouer, nouvPlat), profondeur)
    coordPieceChoisie = 0
    for i, coup in enumerate(piecesCoupPossibles[1:]) :
        nouvPlat = deepcopy(plateau) # utilise un autre plateau pour les tests
        scoreTest = coup_immediat(player, jouer(coup, nouvPlat), profondeur)
        if scoreTest > scoreJouer :
            scoreJouer = scoreTest
            aJouer = coup
            coordPieceChoisie = i

    return coordPieceChoisie, aJouer



def coup_immediat(player, plateau: Plateau, profondeur, tabScores):

    if profondeur==0 or partie_finie :
        return scoreJoueur

    else:
        coup = coup_a_jouer(joueur.joueur_suivant(player), nouvPlat,  profondeur-1)

    scorePlayer, scoreEnnemi = modif_score(joueur.joueur_suivant(player), jouer(coup,nouvPlat), profondeur-1)



    tabScores[0] = scorePlayer
    if scoreEnnemi != None:
        tabScores[scoreEnnemi[0]] = scoreEnnemi[1]



def tab_score(player, plateau: Plateau, profondeur):
    scoreJoueur = player.score
    scoreEnnemi1 = joueur.joueur_suivant(player).score
    scoreEnnemi2 = joueur.joueur_suivant(joueur.joueur_suivant(player)).score
    return [scoreJoueur, scoreEnnemi1, scoreEnnemi2]



def jouer(player, coordPiece, nouvCase, plateau: Plateau):
    """joue un coup sur une copie du plateau et enregistre le score actuel
    Entrée : le coup a jouer c'est a dire la piece et la case sur laquelle elle va
    Sortie : le nouveau plateau (la copie qui a changee) , et le score des joueurs """
    p1, x1, y1 = coordPiece
    p2, x2, y2 = nouvCase

    if isinstance(plateau[p2][x2][y2], Pieces.Piece):
        pieceKill = plateau[p2][x2][y2]
        modif_score(player, coordPiece, nouvCase, plateau, True)

    else :
        plateau.sur_deplacement_valide(coordPiece, nouvCase)
        modif_score(player, coordPiece, nouvCase, plateau, False)

def modif_score(player, coordPiece, nouvCase, plateau, bool):
    """Entrée : player est celui qui joue, piece est la piece a bouger sur nouvCase,
        bool contient 'il y a un ennemi sur la case'
    Sortie : modifie le score en fonction d'un mouvement puis fais le mouvement"""

    p1, x1, y1 = coordPiece
    piece = plateau[p1][x1][y1]
    p2, x2, y2 = nouvCase
    case = plateau[p2][x2][y2]
    platOriPiece = piece.terrainOrigine
    platActPiece = piece.terrainActuel

    differenceTerrain = abs(p1 - p2) % 3

    if differenceTerrain == 0 or platActPiece == platOriPiece:
        scoreSupp1 = piece.scorePiece*(x2-x1)*(y2-y1)
    elif platOriPiece == p2:
        scoreSupp1 = piece.scorePiece*(x2*y2-(5-x1)*(5-y1)) -25
    else :
        scoreSupp1 = piece.scorePiece*((5-x2)*(5-y2)-x1*y1) +25
    #trouve le changement de score de player

    if bool: # verifie si il y a un ennemi
        if case.score == 1:
            nouvScore2 = case.joueur.score
        elif case.terrainOrigine == p2 :
            nouvScore2 = case.scorePiece*x2*y2

        else:
            nouvScore2 = case.scorePiece*((5-x2)*(5-y2)+25)


        if case.joueur == joueur.joueur_suivant(player):
            numScore = 1
        else:
            numScore = 2
        NouvScore2 = case.joueur.score - nouvScore2
        NouvScore1 = score1 + scoreSupp1
        coupleIfEnnemi = (numScore, NouvScore2)
    # trouve le nouveau score dans le cas ou il y a un ennemi


    else : # la case est libre
        NouvScore1 = score1 + scoreSupp1
        coupleIfEnnemi = (None, None, None)
    # trouve le nouveau score dans le cas ou il n'y a pas d'ennemi

    return NouvScore1, coupleIfEnnemi


def jeu_IA(plateau: Plateau, difficulte, IA):
    """fonction principale qui s'occupe de faire jouer l'IA
    Entrée : le plateau qui contient l'etat du jeu,
             la difficulte qui determine le niveau de l'IA c'est a dire combien de tours a l'avance prevoit l'IA
    Precondition : c'est a l'IA de jouer
    Sortie : deplacement de la piece par l'IA"""

    profondeur = 3*difficulte
    # profondeur = nombre de coups d'avance (compte les coups des 3 joueurs)
    # difficulte = nombre de tours de plateau d'avance (ne compte que les fois oÃ¹ l'IA joue)

    numPiece, coupJoue = coup_a_jouer(IA, plateau, profondeur)
    pieceJoue = tabPosPieces[numPiece]
    return pieceJoue, coupJoue


if __name__ == '__main__':
    import Pieces
    from joueur import Joueur, ListeDeJoueurs
    from Interface import ROUGE, VERT, BLEU, BLANC

    listJoueur = ListeDeJoueurs(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT), Joueur("Florian", 2, ROUGE))
    plateau = Plateau(listJoueur)
    print(coup_a_jouer(Joueur("Arthur", 0, BLEU), plateau, 1))
    print(jeu_IA(plateau,1 , Joueur("Arthur", 0, BLEU)))
