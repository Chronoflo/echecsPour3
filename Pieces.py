﻿# Jeu d'Echec pour 3 joueurs
from constantes import *
from fonctions import signe

class GD(tuple):
    def __init__(self, g, d):
        super().__init__((g, d))

class DG(tuple):
    def __init__(self, g, d):
        super().__init__((g, d))

class Piece:
    """ Définit la classe piece, qui définira le comportement général de chaque
    pieces (pions, tours, dame, ...)
    Nom € { pion, dame, tour, ... } """
    def __init__(self, nom, joueur):
        self.nom = nom
        self.joueur = joueur
        self.emplacementInitial = True

class Pion(Piece):
    """ Definit le pion, deplacements autorisés etc... """
    def __init__(self, joueur):
        super().__init__("Pion", joueur)

    def deplacements_possibles(self):
        """ Envois un Booléen (0,1,2 pour respectivement False,True,Rock)
        devant qui dit si le déplacement est infini ou
        fini, le tableau des déplacements fini (vecteur des déplacements
        infinis) possible du Pion.
        Separe le cas où il y a une piece ennemie et où il n'y a rien.
        Avec à la fin le max des déplacements possibles si déplacement infini"""

        tabAvecEnnemis = 0, [ GD(1,1), GD(-1,1), GD(1,-1) ]
        """ La régle de la prise en passant n'est pas présente dans cette
        version """

        if self.emplacementInitial:
            tabSansEnnemis = 1 , [ GD(1,0), GD(0,1) ], 2

        else:
            tabSansEnnemis = 0 , [ GD(1,0), GD(0,1) ]

        return (tabSansEnnemis, tabAvecEnnemis)

class Roi(Piece):
    """ Definit le Roi, deplacements autorisés etc... """
    def __init__(self, joueur):
        super().__init__("Roi", joueur)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Roi
        Avec la possiblilité de rock"""

        tabSansEnnemis = (FINI, [GD(0,1),GD(1,0),GD(-1,0),GD(0,-1), GD(1,1),GD(1,-1),
                            GD(-1,1),GD(-1,-1)] ), GD(ROCK, [GD(2,0), GD(1,0)])

        tabAvecEnnemis = 0 , [(0,1),(1,0),(-1,0),(0,-1),
                             (1,1),(1,-1), (-1,1),(-1,-1)]

        return (tabSansEnnemis, tabAvecEnnemis)

class Cavalier(Piece):
    """ Definit le Roi, deplacements autorisés etc... """
    def __init__(self, joueur):
        super().__init__("Cavalier", joueur)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Cavalier """

        tab = 0, [(2,1), (1,2), (-2,1), (-1,2),
                     (2,-1), (1,-2), (-2,-1), (-1,-2)]

        return (tab, tab)

class Chevre(Piece):
    """ Definit la Chevre, deplacements autorisés etc... (nouvelle piece) """
    def __init__(self, joueur):
        super().__init__("Chevre", joueur)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Chevre """

        tab = 0 , [(2,0), (0,2), (-2,0), (0,-2),
                  (2,2), (-2,-2), (-2,2), (2,-2)]

        return (tab, tab)

class Tour(Piece):
    """ Definit la Tour, deplacements autorisés etc... """
    def __init__(self, joueur):
        super().__init__("Chevre", joueur)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Tour """

        tab = 1 , [(1,0), (0,1), (-1,0), (0,-1)]

        return (tab, tab)

class Fou(Piece):
    """ Definit le Fou, deplacements autorisés etc... """
    def __init__(self, joueur):
        super().__init__("Fou", joueur)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Fou"""

        tab = 1 , [(1,1), (1,-1), (-1,1), (-1,-1)]

        return (tab, tab)

class Reine(Piece):
    """ Definit la Reine, deplacements autorisés etc... """
    def __init__(self, joueur):
        super().__init__("Reine", joueur)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Reine"""

        tab = 1 , [(1,0), (0,1), (-1,0), (0,-1), (1,1), (1,-1), (-1,1), (-1,-1)]

        return (tab, tab)

def fonction_auxiliaire_de_la_mort(tabssE,tabacE,pos, n):
    """ Attention : il n'est pas prévu qu'un déplacement fini permette de changer deux fois
     de plateau dans un même sens. """
    def nouveau_terrain(terrainActuel, modification):
        return (terrainActuel + modification) % 3

    def nv_case(u):
        return 2*n - u - 1

    p, d, g = pos
    depsPossibles = []

    for typeDep, deplacements in tabssE:
        if typeDep == FINI:
            for vecteur in deplacements:
                x, y = vecteur
                i, j = d + x, g + y
                if i >= 0 and j >= 0:
                    if d == g and y == x:
                        # Cas où le pion est sur la diagonale de la mort
                        if i < n:
                            depsPossibles.append((FINI, (p, i, j)))
                    elif i < n and j < n:
                        depsPossibles.append((FINI, (p, i, j)))
                    elif i < n:
                        depsPossibles.append((FINI, (nouveau_terrain(p, 1), nv_case(j), i)))
                    elif g + y < n:
                        depsPossibles.append((FINI, (nouveau_terrain(p, -1), j, nv_case(i))))
                    else:
                        if vecteur is GD:
                            depsPossibles.append((FINI, (nouveau_terrain(p, signe(x * y)),
                                                         nv_case(i), nv_case(j))))
                        else:
                            pass
        elif typeDep == INFINI:
            nCasesMax = deplacements[0]
            for x, y in deplacements[1:]:
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
        elif typeDep == ROCK:
            for x, y in deplacements:
                depsPossibles.append((ROCK, (p, d+x, g+y)))
        else:
            raise ValueError("Type inconnu.")


def test_infini(p, d, g, x, y, n=6, nCasesMax=11):
    """ Fonction de test. """
    def nouveau_terrain(terrainActuel, modification):
        return (terrainActuel + modification) % 3

    def nv_case(u):
        return 2*n - (u+1)

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


print(test_infini(2, 0, 0, 0, 1))
