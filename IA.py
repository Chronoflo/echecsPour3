import Pieces
import joueur
from plateau import Plateau

def trouve_pieces_et_coups_joueur(player, plateau: Plateau):
    """Fonction qui enregistre dans un tableau tous les déplacements possibles de l'IA"""
    piecesCoupPossibles = []
    piecePossible = []
    for p in range(3):
        for x in range(6):
            for y in range(6):
                if isinstance(plateau[p][x][y], Pieces.Piece) and plateau[p][x][y].joueur == player:
                    piece = plateau[p][x][y]
                    position = (p,x,y)
                    depSans, depAvec = Pieces.traduction_en_couples_déplacements(*piece.vecteurs_deplacements_possibles(), position)
                    deplacements = Pieces.dep_effectifs(depSans, depAvec, piece, plateau)
                    piecePossible.append(position)
                    piecesCoupPossibles.append(deplacements)

    return piecePossible, piecesCoupPossibles


def coup_à_jouer(player, plateau: Plateau, profondeur):
    """Entrées : player, plateau
    Précondition : c'est à player de jouer
    Sorties : le prochain coup joué par player"""


    pieces, coups = trouve_pieces_et_coups_joueur(player, plateau)
    nouvPlat = copy_plat(plateau) # utilise un autre plateau pour les tests
    tabcoups = [] # contiendra 2 fois plus de cases que pieces
    for couples in coups:
        tabSSE, tabACE = couples
        if tabSSE:
            tabcoups.append(tabSSE[0][1])
        else :
            tabcoups.append([])
        if tabACE:
            tabcoups.append(tabACE[0][1])
        else :
            tabcoups.append([])

    i=0
    trouvé = False
    while i<(len(pieces)-1) and not(trouvé):
        if tabcoups[2*i] != []:
            trouvé = True
            j = 2*i
            t = int(i/2)
        elif tabcoups[2*i+1] != [] :
            trouvé = True
            j = 2*i+1
            t = int((i-1)/2)
        i+=1
    p,d,g = pieces[t]

    if i==len(pieces): return None
    pieceJoué, coupJoué = pieces[t], tabcoups[j][0]
    jouer(player, pieceJoué, coupJoué, nouvPlat)
    scoreJouer = coup_immediat(player, nouvPlat, profondeur, tab_score(player, plateau))

    for i, coup in enumerate(tabcoups[(i+1):]) :
        nouvPlat = copy_plat(plateau) # utilise un autre plateau pour les tests
        jouer(player, pieceJoué, coupJoué, nouvPlat)
        scoreTest = coup_immediat(player, nouvPlat, profondeur, tab_score(player, plateau))
        if scoreTest > scoreJouer :
            scoreJouer = scoreTest
            coupJoué = tabcoups[i][0]
            pieceJoué = pieces[int(i/2)]

    return pieceJoué, coupJoué


def copy_plat(plateau):
    print(type(plateau))
    """fait une copie du plateau"""
    nouvPlat = Plateau(listJoueur)
    for p in range(3):
        for d in range(6):
            for g in range(6):
                piece = plateau[p][d][g]

                if isinstance(piece, Pieces.Roi):
                    nouvPiece = Pieces.Roi(piece.joueur, piece.terrainOrigine)
                elif isinstance(piece, Pieces.Reine):
                    nouvPiece = Pieces.Reine(piece.joueur, piece.terrainOrigine)
                elif isinstance(piece, Pieces.Fou):
                    nouvPiece = Pieces.Fou(piece.joueur, piece.terrainOrigine)
                elif isinstance(piece, Pieces.Tour):
                    nouvPiece = Pieces.Tour(piece.joueur, piece.terrainOrigine)
                elif isinstance(piece, Pieces.Cavalier):
                    nouvPiece = Pieces.Cavalier(piece.joueur, piece.terrainOrigine)
                elif isinstance(piece, Pieces.Pion):
                    nouvPiece = Pieces.Pion(piece.joueur, piece.terrainOrigine)
                elif isinstance(piece, Pieces.Chat):
                    nouvPiece = Pieces.Chat(piece.joueur, piece.terrainOrigine)
                else:
                    nouvPiece = None

                if nouvPiece is not None :
                    nouvPiece.joueur = piece.joueur
                nouvPlat[p][d][g] = nouvPiece
    return nouvPlat


def coup_immediat(player, plateau: Plateau, profondeur, tabScores):
    if profondeur==0 or player.score == 0 :
        return tabScores[0]

    else:
        pieceJoué, coupJoué = coup_à_jouer(joueur.ListeDeJoueurs.joueur_suivant(listJoueur), plateau,  profondeur-1)
        jouer(player, pieceJoué, coupJoué, plateau)
        scorePlayer, scoreEnnemi = modif_score(joueur.ListeDeJoueurs.joueur_suivant(listJoueur), plateau, profondeur-1)

        tabScores[0] = scorePlayer
        if scoreEnnemi != None:
            tabScores[scoreEnnemi[0]] = scoreEnnemi[1]

        return tabScores[0]


def tab_score(player, plateau: Plateau):
    scoreJoueur = player.score
    scoreEnnemi1 = joueur.ListeDeJoueurs.joueur_suivant(listJoueur).score
    scoreEnnemi2 = joueur.ListeDeJoueurs.joueur_suivant(listJoueur).score
    joueur.ListeDeJoueurs.joueur_suivant(listJoueur)
    return [scoreJoueur, scoreEnnemi1, scoreEnnemi2]



def jouer(player, coordPiece, nouvCase, plateau: Plateau):
    """Joue un coup sur une copie du plateau et enregistre le score actuel
    Entrée : le coup à jouer, c'est à dire la pièce et la case sur laquelle elle va
    Sortie : le nouveau plateau (la copie qui a changé) , et le score des joueurs """
    p1, x1, y1 = coordPiece
    p2, x2, y2 = nouvCase

    if isinstance(plateau[p2][x2][y2], Pieces.Piece):
        modif_score(player, coordPiece, nouvCase, plateau, True)

    else :
        modif_score(player, coordPiece, nouvCase, plateau, False)

    plateau[p1][x1][y1], plateau[p2][x2][y2] = None, plateau[p1][x1][y1]


def modif_score(player, coordPiece, nouvCase, plateau, bool):
    """Entrée : player est celui qui joue, piece est la pièce à bouger sur nouvCase,
        bool contient 'il y a un ennemi sur la case'
    Sortie : modifie le score en fonction d'un mouvement puis fait le mouvement"""
    tabScore = tab_score(player, plateau)

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
    # trouve le changement de score de player

    if bool: # verifie si il y a un ennemi
        if case.scorePiece == 0:
            nouvScore2 = case.joueur.score
        elif case.terrainOrigine == p2 :
            nouvScore2 = case.scorePiece*x2*y2

        else:
            nouvScore2 = case.scorePiece*((5-x2)*(5-y2)+25)


        if case.joueur == joueur.ListeDeJoueurs.joueur_suivant(listJoueur):
            numScore = 1
        else:
            numScore = 2
        NouvScore2 = tabScore[numScore] - nouvScore2
        NouvScore1 =  tabScore[0] + scoreSupp1
        coupleIfEnnemi = (numScore, NouvScore2)
    # trouve le nouveau score dans le cas où il y a un ennemi


    else : # la case est libre
        NouvScore1 = tabScore[0] + scoreSupp1
        coupleIfEnnemi = (None, None)
    # trouve le nouveau score dans le cas où il n'y a pas d'ennemi

    return NouvScore1, coupleIfEnnemi


def jeu_IA(plateau: Plateau, difficulte, IA):
    """Fonction principale qui s'occupe de faire jouer l'IA
    Entrée : le plateau qui contient l'état du jeu,
             la difficulté qui détermine le niveau de l'IA, c'est à dire combien de tours à l'avance prévoit l'IA
    Précondition : c'est à l'IA de jouer
    Sortie : déplacement de la pièce par l'IA"""

    profondeur = 3*difficulte+1
    # profondeur = nombre de coups d'avance (compte les coups des 3 joueurs)
    # difficulte = nombre de tours de plateau d'avance (ne compte que les fois où l'IA joue)

    numPiece, coupJoue = coup_à_jouer(IA, plateau, profondeur)
    pieceJoue = tabPosPieces[numPiece]
    return pieceJoue, coupJoue


##if __name__ == '__main__':
##    import Pieces
##    from joueur import Joueur, ListeDeJoueurs
##    from Interface import ROUGE, VERT, BLEU, BLANC
##
##    J1 = Joueur("Arthur", 0, BLEU)
##    listJoueur = ListeDeJoueurs(J1, Joueur("Sarah", 1, VERT), Joueur("Florian", 2, ROUGE))
##    plateau = Plateau(listJoueur)
##    print(jeu_IA(plateau, 0, J1))
