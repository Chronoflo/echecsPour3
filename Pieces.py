# Jeu d'Echec pour 3 joueurs
from constantes import *
from fonctions import signe
import pygame.image

class SP(tuple):
    """ Classe servant à régler les cas particuliers se déroulant au centre du plateau. """
    def __new__(cls, *args, **kwargs):
        return tuple.__new__(SP, args)


class Piece:
    """ Définit la classe Piece, qui définira le comportement général de chaque
    pièce (pions, tours, dame, ...)
    Nom € { pion, dame, tour, ... }
    Définition des déplacements :
        - trois types de déplacements : FINI, INFINI, ROCK
        - la première coordonnée des déplacements infinis contient le nombre de cases maximal
    """
    piècesCréées = []

    def __init__(self, nom, joueur, terrainOrigine, scorePiece):
        self.nom = nom
        self.joueur = joueur

        self.emplacementInitial = True
        self.terrainOrigine = terrainOrigine
        self.terrainActuel = terrainOrigine

        self.scorePiece = scorePiece
        self.image = None

        Piece.piècesCréées.append(self)

    @classmethod
    def chargeImages(cls):
        for piece in cls.piècesCréées:
            piece.image = pygame.image.load("Image/Pieces/"+str(piece.joueur.couleur.nom)+"_"+str(piece.nom)+".png").convert_alpha()
            # Associe une image à chaque pièce et la charge pour l'affichage. Cette image sera redimensionnée plus tard.

    @classmethod
    def classe_de_méthode(cls):
        pass # permet de faire quelque chose sur toutes les pièces

class Pion(Piece):
    """ Définit le pion, deplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super(Pion, self).__init__("Pion", joueur, terrainOrigine, 1)

    def deplacements_possibles(self):
        """ Renvoie une constante : False,True,Rock
        devant qui dit si le déplacement est infini ou
        fini, le tableau des déplacements finis (vecteurs des déplacements
        infinis) possibles du Pion.
        Sépare le cas où il y a une pièce ennemie et où il n'y a rien.
        Avec au début le max des déplacements possibles si le déplacement est infini"""

        differenceTerrain = abs(self.terrainOrigine - self.terrainActuel) % 3

        if differenceTerrain == 0:
            if self.emplacementInitial:
                tabSansEnnemis = [(INFINI, [2, (1, 0), (0, 1)])]

            else:
                tabSansEnnemis = [(FINI, [(1, 0), (0, 1)])]

            tabAvecEnnemis = [(FINI, [(1, 1), (-1, 1), (1, -1)])]

        elif differenceTerrain == 1:
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

    def __init__(self, joueur, terrainOrigine):
        super(Roi, self).__init__("Roi", joueur, terrainOrigine, 0)

    def deplacements_possibles(self):
        """ Envoie le tableau des déplacements possibles du Roi
        Avec la possibilité de rock"""

        tabSansEnnemis = [(FINI, [(0, 1), (1, 0), (-1, 0), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        if self.emplacementInitial:
            tabSansEnnemis.append((ROCK, [(2, 0), (1, 0)]))

        tabAvecEnnemis = [(FINI, [(0, 1), (1, 0), (-1, 0), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        return tabSansEnnemis, tabAvecEnnemis


class Cavalier(Piece):
    """ Définit le Roi, déplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super(Cavalier, self).__init__("Cavalier", joueur, terrainOrigine, 3)

    def deplacements_possibles(self):
        """ Envoie le tableau des déplacements possibles du Cavalier """

        tab = [(FINI, [(2, 1), (1, 2), (-2, 1), (-1, 2),
                       (2, -1), (1, -2), (-2, -1), (-1, -2), SP(2, 1), SP(1, 2)])]
        return (tab, tab)


class Chat(Piece):
    """ Définit le Chat, déplacements autorisés etc... (nouvelle pièce) """

    def __init__(self, joueur, terrainOrigine):
        super(Chat, self).__init__("Chat", joueur, terrainOrigine, 3)

    def deplacements_possibles(self):
        """ Envoie le tableau des déplacements possibles du Chat """

        tab = [(FINI, [(2, 0), (0, 2), (-2, 0), (0, -2),
                       (2, 2), (-2, -2), (-2, 2), (2, -2)])]

        return (tab, tab)


class Tour(Piece):
    """ Définit la Tour, déplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super(Tour, self).__init__("Tour", joueur, terrainOrigine, 5)

    def deplacements_possibles(self):
        """ Envoie le tableau des déplacements possibles de la Tour """

        tab = [(INFINI, [SANSLIMITE, (1, 0), (0, 1), (-1, 0), (0, -1)])]

        return tab, tab


class Fou(Piece):
    """ Définit le Fou, déplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super(Fou, self).__init__("Fou", joueur, terrainOrigine, 5)

    def deplacements_possibles(self):
        """ Envoie le tableau des déplacements possibles du Fou"""

        tab = [(INFINI, [SANSLIMITE, (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        return (tab, tab)


class Reine(Piece):
    """ Définit la Reine, déplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super(Reine, self).__init__("Reine", joueur, terrainOrigine, 10)

    def deplacements_possibles(self):
        """ Envoie le tableau des déplacements possibles de la Reine"""

        tab = [(INFINI, [SANSLIMITE, (1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1),
                         (-1, 1), (-1, -1)])]

        return (tab, tab)


def traduction_en_couples_déplacements(déplacementsSansEnnemi, déplacementsAvecEnnemi, pos, n=6):
    """
    Sert à passer des couples vecteurs d'une pièce à ses déplacements effectifs par rapport à sa position.
    :param déplacementsSansEnnemi: tableaux contenant les couples vecteurs en cas normal
    :param déplacementsAvecEnnemi: tableaux contenant les couples vecteurs en cas d'ennemis
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
        Coeur de la procédure. Définition : la diagonale de la mort du terrain t correspond à
        la diagonale {(t, i, i), i € R}. Elle a pour propriété particulière de ne pas permettre
        un déplacement de vecteur (1, 1) en case (t, 5, 5).
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
                                if (d, g) == (5, 5):  # les vecteurs SP ne s'appliquent qu'au centre du plateau
                                    depsFini.append((nouveau_terrain(p, -signe(x * y)), nv_case(j), nv_case(i)))

                if depsFini :  # ajout à depsPossibles seulement si depsFini est non vide
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

    return traite(déplacementsSansEnnemi), traite(déplacementsAvecEnnemi)


def dep_effectifs(déplacementsSansEnnemi, déplacementsAvecEnnemi, piece, plateau):
    nom = piece.joueur
    """Effectue les tests pour vérifier s'il y a ou non des ennemis, pour le
    bon déplacement"""
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
                    if not(isinstance(plateau[p][x][y], Piece)):
                        # teste si la case est libre
                        depsFini.append(case)

            elif typeDep == INFINI:
                i = 0
                bloqué = False

                while not(bloqué) and i<len(cases):
                    case = cases[i]
                    p, x, y = case
                    if isinstance(plateau[p][x][y], Piece):
                        # teste si la case est libre
                        bloqué = True
                    else :
                        depsInfini.append(case)
                    i+=1

            elif typeDep == ROCK:
                if piece.emplacementInitial :
                    p, x, y = cases[0]
                    joueur = piece.joueur
                    if joueur.tour1.emplacementInitial and not isinstance(plateau[p][x-1][y],Piece) and nom == plateau[p][x][y].joueur:
                        # teste si la case est libre et si les bonnes pièces sont aux bons endroits sans avoir bougé
                        depsRock.append((p,x,y))

                    p, x, y = cases[1]
                    if joueur.tour2.emplacementInitial and nom == plateau[p][x][y].joueur:
                        # teste si la case est libre et si les bonnes pièces sont aux bons endroits sans avoir bougé
                        depsRock.append((p,x,y))

            else :
                raise ValueError("Type de déplacement inconnu.")


        if depsFini:
            depsPossibles.append((FINI, depsFini))

        if depsInfini:
            depsPossibles.append((INFINI, depsInfini))

        if depsRock :
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

                    if isinstance(plateau[p][x][y], Piece) and (nom != plateau[p][x][y].joueur):
                        depsFini.append(case)

            elif typeDep == INFINI:
                i=0
                bloqué = False
                while not(bloqué) and i<len(cases):
                    case = cases[i]
                    p,x,y = case

                    if isinstance(plateau[p][x][y], Piece):
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


def promotionReine(piece, pos, plateau):
    """procédure plaçant une reine à l'endroit du pion
    le pion doit être au bon endroit pour la promotion"""
    p, d, g = pos
    plateau[p][d][g] = joueur.plateau[p][d][g].Pieces.Reine(self, piece.terrainOrigine)


def test_infini(p, d, g, x, y, n=6, nCasesMax=11):
    """ Fonction de test. """

    def nouveau_terrain(terrainActuel, modification):
        return (terrainActuel + modification) % 3

    def nv_case(u):
        return 2 * n - (u + 1)

    depsInfini = []
    i, j = d + x, g + y
    k = 1
    while 0 <= i < n and 0 <= j < n and k < nCasesMax:
        depsInfini.append((p, i, j))
        i += x
        j += y

        if i < n <= j:
            p, i, j = nouveau_terrain(p, 1), nv_case(j), i
            x, y = -y, x
        elif j < n <= i:
            p, i, j = nouveau_terrain(p, -1), j, nv_case(i)
            x, y = y, -x

        k += 1
    return depsInfini

##if __name__ == '__main__':
##    import Pieces
##    from plateau import Plateau
##    from joueur import Joueur, ListeDeJoueurs
##    from Interface import ROUGE, VERT, BLEU
##
##    depssE, depacE = traduction_en_couples_déplacements(*Tour.deplacements_possibles(None), (0, 0, 5), 6)
##    listJoueur = ListeDeJoueurs(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT),
##                                  Joueur("Florian", 2, ROUGE))
##    Tour.joueur = Joueur("Arthur", 0, BLEU)
##    plateau = Plateau(listJoueur)
##    print(isinstance(plateau[0][0][0], Pieces.Piece))
##    print(dep_effectifs(depssE, depacE, Tour, plateau))

if __name__ == '__main__':
    import Pieces
    from plateau import Plateau
    from joueur import Joueur, ListeDeJoueurs
    from Interface import ROUGE, VERT, BLEU, BLANC


    depssE, depacE = traduction_en_couples_déplacements(*Tour.deplacements_possibles(None), (0, 0, 5), 6)
    listJoueur = ListeDeJoueurs(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT), Joueur("Florian", 2, ROUGE))
    Tour.joueur = Joueur("Arthur", 0, BLEU)
    plateau = Plateau(listJoueur)
    print(isinstance(plateau[0][0][0], Pieces.Piece))
    print(dep_effectifs(depssE, depacE, Tour, plateau))
