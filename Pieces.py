# Jeu d'Echec pour 3 joueurs
from constantes import *
from fonctions import signe
import pygame.image


class GD(tuple):
    def __new__(self, x, y):
        return tuple.__new__(GD, (x, y))


class DG(tuple):
    def __init__(self, *args):
        super().__init__()


class Piece:
    """ Définit la classe piece, qui définira le comportement général de chaque
    pieces (pions, tours, dame, ...)
    Nom € { pion, dame, tour, ... }
    Définition des déplacements :
        - trois types de déplacements : FINI, INFINI, ROCK
        - la première coordonnées des déplacements infinis contient le nombre de cases maximal
    """
    piècesCréées = []

    def __init__(self, nom, joueur, terrainOrigine):
        self.nom = nom
        self.joueur = joueur

        self.emplacementInitial = True
        self.terrainOrigine = terrainOrigine
        self.terrainActuel = terrainOrigine

        Piece.piècesCréées.append(self)

    @classmethod
    def charge_images(cls):
        for piece in cls.piècesCréées:
            pass


class Pion(Piece):
    """ Definit le pion, deplacements autorisés etc... """
    def __init__(self, joueur, terrainOrigine):
        super().__init__("Pion", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois une constante : False,True,Rock
        devant qui dit si le déplacement est infini ou
        fini, le tableau des déplacements fini (vecteur des déplacements
        infinis) possible du Pion.
        Separe le cas où il y a une piece ennemie et où il n'y a rien.
        Avec à la fin le max des déplacements possibles si déplacement infini"""

        DifferenceTerrain = (abs(self.terrainOrigine - self.terrainActuel)) % 3

        if DifferenceTerrain == 0:
            if self.emplacementInitial:
                tabSansEnnemis = [(INFINI , [2, GD(1,0), GD(0,1) ])]

            else:
                tabSansEnnemis = [(FINI , [ GD(1,0), GD(0,1) ])]

            tabAvecEnnemis = [(FINI , [ GD(1,1), GD(-1,1), GD(1,-1) ])]


        elif DifferenceTerrain == 1:
            tabSansEnnemis = [(FINI , [ GD(0,-1) ])]

            tabAvecEnnemis = [(FINI , [ GD(-1,-1), GD(1,-1) ])]


        else :
            tabSansEnnemis =  [(FINI , [ GD(-1,0) ])]

            tabAvecEnnemis = [(FINI , [ GD(-1,-1), GD(-1,1) ])]


        """ La régle de la prise en passant n'est pas présente dans cette
        version """

        return (tabSansEnnemis, tabAvecEnnemis)

class Roi(Piece):
    """ Definit le Roi, deplacements autorisés etc... """
    def __init__(self, joueur, terrainOrigine):
        super().__init__("Roi", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Roi
        Avec la possiblilité de rock"""

        tabSansEnnemis = [(FINI, [GD(0,1),GD(1,0),GD(-1,0),GD(0,-1), GD(1,1),GD(1,-1),
                            GD(-1,1),GD(-1,-1)] ), (ROCK, [GD(2,0), GD(1,0)])]

        tabAvecEnnemis = [(FINI , [GD(0,1), GD(1,0), GD(-1,0), GD(0,-1),
                                GD(1,1), GD(1,-1), GD(-1,1), GD(-1,-1)])]

        return (tabSansEnnemis, tabAvecEnnemis)

class Cavalier(Piece):
    """ Definit le Roi, deplacements autorisés etc... """
    def __init__(self, joueur, terrainOrigine):
        super().__init__("Cavalier", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Cavalier """

        tab = [(FINI, [GD(2,1), GD(1,2), GD(-2,1), GD(-1,2),
                     GD(2,-1), GD(1,-2), GD(-2,-1), GD(-1,-2)])]

        return (tab, tab)

class Chevre(Piece):
    """ Definit la Chevre, deplacements autorisés etc... (nouvelle piece) """
    def __init__(self, joueur, terrainOrigine):
        super().__init__("Chevre", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Chevre """

        tab = [(FINI , [GD(2,0), GD(0,2), GD(-2,0), GD(0,-2),
                     GD(2,2), GD(-2,-2), GD(-2,2), GD(2,-2)])]

        return (tab, tab)

class Tour(Piece):
    """ Definit la Tour, deplacements autorisés etc... """
    def __init__(self, joueur, terrainOrigine):
        super().__init__("Chevre", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Tour """

        tab = [(INFINI , [SANSLIMITE, GD(1, 0), GD(0, 1), GD(-1, 0), GD(0, -1)])]

        return tab, tab

class Fou(Piece):
    """ Definit le Fou, deplacements autorisés etc... """
    def __init__(self, joueur, terrainOrigine):
        super().__init__("Fou", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Fou"""

        tab = [(INFINI , [SANSLIMITE, GD(1, 1), GD(1, -1), GD(-1, 1), GD(-1, -1)])]

        return (tab, tab)

class Reine(Piece):
    """ Definit la Reine, deplacements autorisés etc... """
    def __init__(self, joueur, terrainOrigine):
        super().__init__("Reine", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Reine"""

        tab = [(INFINI , [SANSLIMITE, GD(1, 0), GD(0, 1), GD(-1, 0), GD(0, -1), GD(1, 1), GD(1, -1),
                          GD(-1,1), GD(-1,-1)])]

        return (tab, tab)


def traduction_en_coordonnées(déplacementsSansEnnemi, déplacementsAvecEnnemi, pos, n):
    """ Attention : il n'est pas prévu qu'un déplacement fini permette de changer deux fois
     de plateau dans un même sens. """
    def nouveau_terrain(terrainActuel, modification):
        return (terrainActuel + modification) % 3

    def nv_case(u):
        return 2*n - u - 1

    def traite(déplacements):
        p, d, g = pos
        depsPossibles = []

        for typeDep, deplacements in déplacements:
            if typeDep == FINI:
                for vecteur in deplacements:
                    x, y = vecteur
                    i, j = d + x, g + y
                    if i >= 0 and j >= 0:
                        if d == g and y == x:
                            # Cas où la pièce est sur la diagonale de la mort
                            if i < n:
                                depsPossibles.append((FINI, (p, i, j)))
                        elif i < n and j < n:
                            # Cas où le déplacement ne dépasse pas
                            depsPossibles.append((FINI, (p, i, j)))
                        elif i < n:
                            # Cas où le déplacement dépasse du côté gauche du terrain
                            depsPossibles.append((FINI, (nouveau_terrain(p, 1), nv_case(j), i)))
                        elif g + y < n:
                            # Cas où le déplacement dépasse du côté droit
                            depsPossibles.append((FINI, (nouveau_terrain(p, -1), j, nv_case(i))))
                        else:
                            # Cas où le déplacement dépasse des deux côtés
                            if vecteur is GD:
                                depsPossibles.append((FINI, (nouveau_terrain(p, signe(x * y)),
                                                             nv_case(i), nv_case(j))))
                            else:
                                pass  # TODO
            elif typeDep == INFINI:
                if deplacements[0] == SANSLIMITE:
                    nCasesMax = 2 * n - 1
                else:
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
                    if depsInfini:
                        depsPossibles.append((INFINI, depsInfini))
            elif typeDep == ROCK:
                for x, y in deplacements:
                    depsPossibles.append((ROCK, (p, d + x, g + y)))
            else:
                raise ValueError("Type inconnu.")

        return depsPossibles

    return traite(déplacementsSansEnnemi), traite(déplacementsAvecEnnemi)


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


if __name__ == '__main__':
    # print(test_infini(2, 0, 0, 0, 1))
    print(traduction_en_coordonnées(*Tour.deplacements_possibles(2), (0, 0,0), 6))
