﻿from constantes import *
from fonctions import signe
import pygame.image


class SP(tuple):
    """ Couple servant à régler les cas particuliers se déroulant au centre du plateau. """
    def __new__(cls, *args, **kwargs):
        return tuple.__new__(SP, args)


class Piece:
    """
    Définit la classe Piece, qui définira le comportement général de chaque pièce (pions, tours, dame, ...).

    Définition des déplacements :
        - trois types de déplacements : FINI, INFINI, ROCK
        - la première coordonnée des déplacements infinis contient le nombre de cases maximal
    """
    piècesCréées = []

    def __init__(self, nom, joueur, terrainDOrigine, scorePiece, image=None):
        """
        Crée une pièce.
        :param nom: nom de la pièce
        :param joueur: joueur qui possède la pièce
        :param terrainDOrigine:
        :param scorePiece: valeur de la pièce
        :param image:
        """
        self.nom = nom
        self.joueur = joueur

        self.emplacementInitial = True
        self.terrainOrigine = terrainDOrigine
        self.terrainActuel = terrainDOrigine

        self.scorePiece = scorePiece
        self.image = image

        Piece.piècesCréées.append(self)

    def déplacements_possibles(self, pos, plateau):
        """ Renvoie les tableaux sans et avec ennemi des déplacements possibles de la pièce. """
        return deps_possibles(*traduction_en_couples_déplacements(*self.vecteurs_déplacements(), pos), self, plateau)

    def vecteurs_déplacements(self):
        """ Renvoie deux tableaux contenant les vecteurs déplacement sans et avec ennemi de la pièce. """
        return [], []

    @classmethod
    def chargeImages(cls):
        """ Charge les images de toutes les pièces. """
        for piece in cls.piècesCréées:
            piece.image = pygame.image.load("Image/Pieces/"+str(piece.joueur.couleur.nom)+"_"+str(piece.nom)+".png").convert_alpha()
            # Associe une image à chaque pièce et la charge pour l'affichage. Cette image sera redimensionnée plus tard.


class Pion(Piece):
    """ Définit le pion, deplacements autorisés etc... """

    def __init__(self, joueur, terrainDOrigine):
        super(Pion, self).__init__("Pion", joueur, terrainDOrigine, 1)

    def vecteurs_déplacements(self):
        """ Les vecteurs sont adaptés en fonction du terrain actuel. """

        differenceTerrain = (self.terrainOrigine - self.terrainActuel) % 3

        if differenceTerrain == 0:
            if self.emplacementInitial:
                tabSansEnnemis = [(INFINI, [2, (1, 0), (0, 1)])]

            else:
                tabSansEnnemis = [(FINI, [(1, 0), (0, 1)])]

            tabAvecEnnemis = [(FINI, [(1, 1), (-1, 1), (1, -1)])]

        elif differenceTerrain == 2:
            tabSansEnnemis = [(FINI, [(-1, 0)])]

            tabAvecEnnemis = [(FINI, [(-1, -1), (-1, 1)])]

        else:
            tabSansEnnemis = [(FINI, [(0, -1)])]

            tabAvecEnnemis = [(FINI, [(-1, -1), (1, -1)])]

        """ La règle de la prise en passant n'est pas présente dans cette
        version """

        return tabSansEnnemis, tabAvecEnnemis


class Roi(Piece):
    """ Définit le Roi, déplacements autorisés etc... """

    def __init__(self, joueur, terrainDOrigine):
        super(Roi, self).__init__("Roi", joueur, terrainDOrigine, 0)

    def vecteurs_déplacements(self):
        """ Le rock n'est possible que si le roi n'a pas été bougé. """

        tabSansEnnemis = [(FINI, [(0, 1), (1, 0), (-1, 0), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        if self.emplacementInitial:
            tabSansEnnemis.append((ROCK, [(2, 0), (0, 1)]))

        tabAvecEnnemis = [(FINI, [(0, 1), (1, 0), (-1, 0), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        return tabSansEnnemis, tabAvecEnnemis


class Cavalier(Piece):
    """ Définit le Roi, déplacements autorisés etc... """

    def __init__(self, joueur, terrainDOrigine):
        super(Cavalier, self).__init__("Cavalier", joueur, terrainDOrigine, 3)

    def vecteurs_déplacements(self):
        """ Utilise des vecteurs SP pour règler les cas particuliers au centre. """

        tab = [(FINI, [(2, 1), (1, 2), (-2, 1), (-1, 2),
                       (2, -1), (1, -2), (-2, -1), (-1, -2), SP(2, 1), SP(1, 2)])]
        return tab, tab


class Chat(Piece):
    """ Définit le Chat, déplacements autorisés etc... (nouvelle pièce) """

    def __init__(self, joueur, terrainDOrigine):
        super(Chat, self).__init__("Chat", joueur, terrainDOrigine, 3)

    def vecteurs_déplacements(self):
        tab = [(FINI, [(2, 0), (0, 2), (-2, 0), (0, -2),
                       (2, 2), (-2, -2), (-2, 2), (2, -2)])]

        return tab, tab


class Tour(Piece):
    """ Définit la Tour, déplacements autorisés etc... """

    def __init__(self, joueur, terrainDOrigine):
        super(Tour, self).__init__("Tour", joueur, terrainDOrigine, 5)

    def vecteurs_déplacements(self):
        tab = [(INFINI, [SANSLIMITE, (1, 0), (0, 1), (-1, 0), (0, -1)])]

        return tab, tab


class Fou(Piece):
    """ Définit le Fou, déplacements autorisés etc... """

    def __init__(self, joueur, terrainDOrigine):
        super(Fou, self).__init__("Fou", joueur, terrainDOrigine, 5)

    def vecteurs_déplacements(self):
        tab = [(INFINI, [SANSLIMITE, (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        return tab, tab


class Reine(Piece):
    """ Définit la Reine, déplacements autorisés etc... """

    def __init__(self, joueur, terrainDOrigine, image=None):
        super(Reine, self).__init__("Reine", joueur, terrainDOrigine, 10, image)

    def vecteurs_déplacements(self):
        tab = [(INFINI, [SANSLIMITE, (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1),
                         (-1, 1), (-1, -1)])]

        return tab, tab


def traduction_en_couples_déplacements(vecteursSansEnnemi, vecteursAvecEnnemi, pos, n=6):
    """
    Sert à passer des couples vecteurs d'une pièce à ses déplacements effectifs par rapport à sa position.
    :param vecteursSansEnnemi: tableaux contenant les couples vecteurs en cas normal
    :param vecteursAvecEnnemi: tableaux contenant les couples vecteurs en cas d'ennemis
    :param pos: position de la pièce
    :param n: nombre de cases d'un côté
    :return: deux tableaux, celui des couples déplacements en cas normal et celui des couples déplacements en cas d'ennemi
    """

    def nouveau_terrain(terrainActuel, modification):
        """ Passe d'un terrain à l'autre selon modification. """
        return (terrainActuel + modification) % 3

    def nv_case(u):
        """ Sert à calculer les nouvelles coordonnées d'une case lors d'un changement de terrain. """
        return 2 * n - u - 1

    def traite(couplesVecteurs):
        """
        Coeur de la procédure.
        Petite définition : la diagonale de la mort du terrain t correspond à la diagonale {(t, i, i), i € R}.
        Elle a pour propriété particulière de ne pas permettre un déplacement de vecteur (1, 1) en case (t, 5, 5).
        """
        p, d, g = pos
        depsPossibles = []  # contiendra le résultat final de traite

        for typeDep, vecteurs in couplesVecteurs:
            if typeDep == FINI:
                depsFini = []
                for vecteur in vecteurs:
                    # Application du vecteur
                    x, y = vecteur
                    i, j = d + x, g + y

                    # Corrrection des coordonnées
                    if 0 <= i < 2 * n and 0 <= j < 2 * n:  # pas de sortie du plateau
                        if d == g and y == x:  # pièce sur la diagonale de la mort
                            if i < n:
                                depsFini.append((p, i, j))

                        elif i < n and j < n:
                            depsFini.append((p, i, j))  # pas de dépassement

                        elif i < n:
                            depsFini.append((nouveau_terrain(p, 1), nv_case(j), i))  # dépassement à gauche

                        elif g + y < n:
                            depsFini.append((nouveau_terrain(p, -1), j, nv_case(i)))  # dépassement à droite

                        else:  # double dépassement
                            # en cas de double dépassement on peut avoir besoin du cas SP pour gérer les situations
                            # au centre
                            if not isinstance(vecteur, SP):  # vecteur de type quelconque
                                depsFini.append((nouveau_terrain(p, signe(x * y)), nv_case(i), nv_case(j)))
                            else:
                                if min(d, g) >= 4:  # les vecteurs SP ne s'appliquent qu'au centre du plateau
                                    depsFini.append((nouveau_terrain(p, -signe(x * y)), nv_case(j), nv_case(i)))

                if depsFini:  # ajout à depsPossibles seulement si depsFini est non vide
                    depsPossibles.append((FINI, depsFini))

            elif typeDep == INFINI:
                if vecteurs[0] == SANSLIMITE:
                    # le déplacement est illimité, on met nCasesMax au maximum possible
                    nCasesMax = 2 * n - 1
                else:
                    nCasesMax = vecteurs[0]

                for x, y in vecteurs[1:]:
                    depsInfini = []
                    t, i, j = p, d + x, g + y
                    k = 1

                    while 0 <= i <= n and 0 <= j <= n and not (i == j == n) and k < nCasesMax + 1:
                        # on ne rentre pas dans la boucle en cas de sortie du plateau (i < 0, j < 0),
                        # ou de dépassement sur la diagonale de la mort => aucune case n'est ajouté

                        # première étape, correction des coordonnées, mise à jour des vecteurs
                        # (pas de possibilité de double dépassement car 0 <= x, y <= 1)

                        if i < n <= j:  # dépassement à gauche
                            t, i, j = nouveau_terrain(t, 1), nv_case(j), i
                            x, y = -y, x  # mise à jour des vecteurs

                        elif j < n <= i:  # dépassement à droite
                            t, i, j = nouveau_terrain(t, -1), j, nv_case(i)
                            x, y = y, -x

                        # deuxième étape, ajout au tableau, incrémentation des variables
                        depsInfini.append((t, i, j))
                        i += x
                        j += y
                        k += 1

                    if depsInfini:
                        depsPossibles.append((INFINI, depsInfini))

            elif typeDep == ROCK:
                # Ici le code est simple car un Rock ne permet pas de changer de terrain
                depsRock = []
                for x, y in vecteurs:
                    depsRock.append((p, d + x, g + y))

                if depsRock:
                    depsPossibles.append((ROCK, depsRock))

            else:
                raise ValueError("Type de déplacement inconnu.")
        return depsPossibles

    return traite(vecteursSansEnnemi), traite(vecteursAvecEnnemi)


def deps_possibles(déplacementsSansEnnemi, déplacementsAvecEnnemi, piece, plateau):
    """
    Renvoie les tableaux sans et avec ennemi des déplacements possibles parmi déplacementsSansEnnemi et
    déplacementsAvecEnnemi.
    """
    nom = piece.joueur

    def traite_sans_ennemis(couplesVecteurs):
        # traite le cas sans ennemi
        depsPossibles = []  # contiendra le résultat final de traite
        depsFini = []
        depsInfini = []
        depsRock = []

        for typeDep, cases in couplesVecteurs:
            if typeDep == FINI:
                for case in cases:
                    p,x,y = case
                    if plateau[p][x][y] == None:
                        # teste si la case est libre
                        depsFini.append(case)

            elif typeDep == INFINI:
                i = 0
                bloqué = False

                while not(bloqué) and i<len(cases):
                    case = cases[i]
                    p, x, y = case
                    if plateau[p][x][y] != None:
                        # teste si la case est libre
                        bloqué = True
                    else :
                        depsInfini.append(case)
                    i+=1

            elif typeDep == ROCK:
                if piece.emplacementInitial:
                    p, x, y = cases[0]
                    joueur = piece.joueur
                    if joueur.tour1 is not None and joueur.tour1.emplacementInitial and plateau[p][x-1][y] is None and nom == plateau[p][x][y].joueur:
                        # teste si la case est libre et si les bonnes pièces sont aux bons endroits sans avoir bougé
                        depsRock.append((p,x,y))

                    p, x, y = cases[1]
                    if joueur.tour2 is not None and joueur.tour2.emplacementInitial and nom == plateau[p][x][y].joueur:
                        # teste si la case est libre et si les bonnes pièces sont aux bons endroits sans avoir bougé
                        depsRock.append((p,x,y))

            else:
                raise ValueError("Type de déplacement inconnu.")

        if depsFini:
            depsPossibles.append((FINI, depsFini))

        if depsInfini:
            depsPossibles.append((INFINI, depsInfini))

        if depsRock:
            depsPossibles.append((ROCK, depsRock))

        return depsPossibles

    def traite_avec_ennemis(couplesVecteurs):
        # traite le cas avec un ennemi
        depsPossibles = []  # contiendra le résultat final de traite
        depsFini = []
        depsInfini = []

        for typeDep, cases in couplesVecteurs:
            if typeDep == FINI:
                for case in cases:
                    p,x,y = case

                    if plateau[p][x][y]!=None and (nom != plateau[p][x][y].joueur):
                        depsFini.append(case)

            elif typeDep == INFINI:
                i=0
                bloqué = False
                while not(bloqué) and i<len(cases):
                    case = cases[i]
                    p,x,y = case

                    if plateau[p][x][y] != None:
                        bloqué = True
                        if nom != plateau[p][x][y].joueur:
                            depsInfini.append(case)
                    i+=1

            else :
                raise ValueError("Type de déplacement inconnu.")
                # Un déplacement de type ROCK ne peut pas prendre de pièce

        if depsFini:
            depsPossibles.append((FINI, depsFini))

        if depsInfini:
            depsPossibles.append((INFINI, depsInfini))

        return depsPossibles

    return traite_sans_ennemis(déplacementsSansEnnemi), traite_avec_ennemis(déplacementsAvecEnnemi)


def promotion_reine(piece):
    """ Renvoie un pion promu en reine. """
    joueur = piece.joueur
    joueur.piecesRestantes.remove(piece)
    piece = Reine(piece.joueur, piece.terrainOrigine, joueur.reine.image)
    joueur.piecesRestantes.append(piece)
    return piece


if __name__ == '__main__':
    from plateau import Plateau
    from joueur import Joueur, ListeDeJoueurs
    from Interface import ROUGE, VERT, BLEU, BLANC

    J1 = Joueur("Arthur", 0, BLEU)
    depssE, depacE = traduction_en_couples_déplacements(*Tour.vecteurs_déplacements(None), (0, 4, 5), 6)
    listJoueur = ListeDeJoueurs(J1, Joueur("Sarah", 1, VERT), Joueur("Florian", 2, ROUGE))
    Tour.joueur = J1

    plateau = Plateau(listJoueur)
    print(deps_possibles(depssE, depacE, Tour, plateau))
