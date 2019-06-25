from time import sleep

from fonctions import concat
from joueur import ListeDeJoueurs, Joueur
from Pieces import Cavalier, traduction_en_couples_déplacements, Piece, Chat, Roi, Fou, Pion, Reine, dep_effectifs, Tour
from plateau import Plateau


def coup_IA(plateau: Plateau, profondeur):
    """Fonction principale qui s'occupe de faire jouer l'IA
    Entrée : le plateau qui contient l'état du jeu,
             la difficulté qui détermine le niveau de l'IA, c'est à dire combien de tours à l'avance prévoit l'IA
    Précondition : c'est à l'IA de jouer
    Sortie : déplacement de la pièce par l'IA"""

    # profondeur = nombre de coups d'avance (compte les coups des 3 joueurs)
    # difficulte = nombre de tours de plateau d'avance (ne compte que les fois où l'IA joue)
    sleep(0.5)
    return coup_à_jouer(plateau.listeJoueurs.joueur_actuel(), plateau, profondeur)


def coup_à_jouer_ancien(player, plateau: Plateau, profondeur):
    """Entrées : player, plateau
    Précondition : c'est à player de jouer
    Sorties : le prochain coup joué par player"""

    pieces, coups = pieces_et_coups(player, plateau)
    nouvPlat = copy_plat(plateau)  # utilise un autre plateau pour les tests
    tabcoups = []  # contiendra 2 fois plus de cases que pieces
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


def trouve_pieces_et_coups_joueur_ancien(player, plateau: Plateau):
    """Fonction qui enregistre dans un tableau tous les déplacements possibles de l'IA"""
    piecesCoupPossibles = []
    positionsPieces = []
    for p in range(3):
        for x in range(6):
            for y in range(6):
                if isinstance(plateau[p][x][y], Piece) and plateau[p][x][y].joueur == player:
                    piece = plateau[p][x][y]
                    position = (p,x,y)
                    depsSans, depsAvec = traduction_en_couples_déplacements(*piece.vecteurs_deplacements_possibles(), position)
                    déplacements = dep_effectifs(depsSans, depsAvec, piece, plateau)
                    positionsPieces.append(position)
                    piecesCoupPossibles.append(déplacements)

    return positionsPieces, piecesCoupPossibles


def coup_à_jouer(joueur, plateau: Plateau, profondeur):
    """
    Renvoie le coup que l'IA doit jouer grâce à une analyse exaustive des posibilités. L'analyse peut se
    faire sur plusieurs niveaux de profondeur.
    """
    score_max = float('-inf')
    meilleur_coup = None

    for pos, déps in pieces_et_coups(joueur, plateau):
        for dép in déps:
            score_dép = score(copy_plat(plateau), profondeur - 1, pos, dép)
            if score_dép > score_max:
                score_max = score_dép
                meilleur_coup = (pos, dép)
    return meilleur_coup


def pieces_et_coups(player, plateau: Plateau):
    """ Renvoie un tableau qui pour chaque pièce contient un couple (positionPièce, DdéplacementsPièces). """
    res = []
    for p in range(3):
        for d in range(6):
            for g in range(6):
                if isinstance(plateau[p][d][g], Piece) and plateau[p][d][g].joueur == player:
                    piece = plateau[p][d][g]
                    pos = (p, d, g)
                    depsSans, depsAvec = piece.déplacements_possibles(pos, plateau)

                    res.append((pos, concat([déps for pos, déps in depsSans + depsAvec])))
    return res


def score(plateau: Plateau, profondeur, posPiece, posCible):
    joueur = plateau.listeJoueurs.joueur_actuel()
    if profondeur > 2:
        print(profondeur)
    def meilleur_score():
        score_max = float('-inf')
        for pos, déps in pieces_et_coups(joueur, plateau):
            for dép in déps:
                score_dép = score(copy_plat(plateau), profondeur - 1, pos, dép)

                if score_dép > score_max:
                    score_max = score_dép

        return score_max

    if profondeur <= 0 or joueur.score == 0:
        return joueur.score
    else:
        nouvScore, scoresEnnemis = modif_score(joueur, posPiece, posCible, plateau, isinstance(plateau.case(posCible), Piece) and joueur.nom == plateau.case(posCible).nom)
        plateau.sur_déplacement_validé(posPiece, posCible)
        joueur.score = nouvScore
        plateau.listeJoueurs.joueur_suivant()
        return meilleur_score()


def copy_plat(plateau):
    """fait une copie du plateau"""
    nouvPlat = Plateau(ListeDeJoueurs(copie_de=plateau.listeJoueurs))
    nouvJoueurs = {joueur.nom: nouvJoueur for joueur, nouvJoueur in zip(plateau.listeJoueurs, nouvPlat.listeJoueurs)}
    for p in range(3):
        for d in range(6):
            for g in range(6):
                if isinstance(plateau[p][d][g], Piece):
                    piece = plateau[p][d][g]
                    if piece.joueur.nom in nouvJoueurs:
                        nouvJoueur = nouvJoueurs[piece.joueur.nom]
                    else:
                        nouvJoueur = piece.joueur

                    if isinstance(piece, Roi):
                        nouvPiece = Roi(nouvJoueur, piece.terrainOrigine)
                    elif isinstance(piece, Reine):
                        nouvPiece = Reine(nouvJoueur, piece.terrainOrigine)
                    elif isinstance(piece, Fou):
                        nouvPiece = Fou(nouvJoueur, piece.terrainOrigine)
                    elif isinstance(piece, Tour):
                        nouvPiece = Tour(nouvJoueur, piece.terrainOrigine)
                    elif isinstance(piece, Cavalier):
                        nouvPiece = Cavalier(nouvJoueur, piece.terrainOrigine)
                    elif isinstance(piece, Pion):
                        nouvPiece = Pion(nouvJoueur, piece.terrainOrigine)
                    elif isinstance(piece, Chat):
                        nouvPiece = Chat(nouvJoueur, piece.terrainOrigine)
                    nouvPiece.terrainActuel = piece.terrainActuel
                    nouvPiece.emplacementInitial = piece.emplacementInitial
                else:
                    nouvPiece = None
                nouvPlat[p][d][g] = nouvPiece
    return nouvPlat


def coup_immediat(player, plateau: Plateau, profondeur, tabScores):
    if profondeur==0 or player.score == 0 :
        return tabScores[0]

    else:
        pieceJoué, coupJoué = coup_à_jouer(ListeDeJoueurs.joueur_suivant(plateau.listeJoueurs), plateau, profondeur - 1)
        jouer(player, pieceJoué, coupJoué, plateau)
        scorePlayer, scoreEnnemi = modif_score(ListeDeJoueurs.joueur_suivant(plateau.listeJoueurs), plateau, profondeur - 1)

        tabScores[0] = scorePlayer
        if scoreEnnemi != None:
            tabScores[scoreEnnemi[0]] = scoreEnnemi[1]

        return tabScores[0]


def tab_score(player, plateau: Plateau):
    scoreJoueur = player.score
    scoreEnnemi1 = ListeDeJoueurs.joueur_suivant(plateau.listeJoueurs).score
    scoreEnnemi2 = ListeDeJoueurs.joueur_suivant(plateau.listeJoueurs).score
    ListeDeJoueurs.joueur_suivant(plateau.listeJoueurs)
    return [scoreJoueur, scoreEnnemi1, scoreEnnemi2]



def jouer(player, coordPiece, nouvCase, plateau: Plateau):
    """Joue un coup sur une copie du plateau et enregistre le score actuel
    Entrée : le coup à jouer, c'est à dire la pièce et la case sur laquelle elle va
    Sortie : le nouveau plateau (la copie qui a changé) , et le score des joueurs """
    p1, x1, y1 = coordPiece
    p2, x2, y2 = nouvCase

    if isinstance(plateau[p2][x2][y2], Piece):
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


        if case.joueur == ListeDeJoueurs.joueur_suivant(plateau.listeJoueurs):
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



if __name__ == '__main__':
   import Pieces
   from joueur import Joueur, ListeDeJoueurs
   from Interface import ROUGE, VERT, BLEU, BLANC

   J1 = Joueur("Arthur", 0, BLEU)
   listeJoueurs = ListeDeJoueurs(J1, Joueur("Sarah", 1, VERT), Joueur("Florian", 2, ROUGE))
   plateau = Plateau(listeJoueurs)
   plateau.sur_déplacement_validé(*coup_IA(plateau, 2))
   listeJoueurs.joueur_suivant()
   print(*coup_IA(plateau, 2))
