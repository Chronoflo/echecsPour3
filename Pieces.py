# Jeu d'Echec pour 3 joueurs
from constantes import *
from fonctions import signe
import pygame.image


class SP(tuple):
    """ Classe servant à régler les cas particuliers se déroulant au centre du plateau. """
    def __new__(cls, *args, **kwargs):
        return tuple.__new__(SP, args)


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

        differenceTerrain = (abs(self.terrainOrigine - self.terrainActuel)) % 3

        if differenceTerrain == 0:
            if self.emplacementInitial:
                tabSansEnnemis = [(INFINI, [2, (1, 0), (0, 1)])]

            else:
                tabSansEnnemis = [(FINI, [(1, 0), (0, 1)])]

            tabAvecEnnemis = [(FINI, [(1, 1), (-1, 1), (1, -1)])]

        elif differenceTerrain == 1:
            tabSansEnnemis = [(FINI, [(0, -1)])]

            tabAvecEnnemis = [(FINI, [(-1, -1), (1, -1)])]

        else:
            tabSansEnnemis = [(FINI, [(-1, 0)])]

            tabAvecEnnemis = [(FINI, [(-1, -1), (-1, 1)])]

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

        tabSansEnnemis = [(FINI, [(0, 1), (1, 0), (-1, 0), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        if self.emplacementInitial:
            tabSansEnnemis.append((ROCK, [(2, 0), (1, 0)]))

        tabAvecEnnemis = [(FINI, [(0, 1), (1, 0), (-1, 0), (0, -1),
                                  (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        return tabSansEnnemis, tabAvecEnnemis


class Cavalier(Piece):
    """ Definit le Roi, deplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super().__init__("Cavalier", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Cavalier """

        tab = [(FINI, [(2, 1), (1, 2), (-2, 1), (-1, 2),
                       (2, -1), (1, -2), (-2, -1), (-1, -2), SP(2, 1), SP(1, 2)])]
        print(*[type(vect) for vect in tab[0][1]])
        return (tab, tab)


class Chevre(Piece):
    """ Definit la Chevre, deplacements autorisés etc... (nouvelle piece) """

    def __init__(self, joueur, terrainOrigine):
        super().__init__("Chevre", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Chevre """

        tab = [(FINI, [(2, 0), (0, 2), (-2, 0), (0, -2),
                       (2, 2), (-2, -2), (-2, 2), (2, -2)])]

        return (tab, tab)


class Tour(Piece):
    """ Definit la Tour, deplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super().__init__("Chevre", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Tour """

        tab = [(INFINI, [SANSLIMITE, (1, 0), (0, 1), (-1, 0), (0, -1)])]

        return tab, tab


class Fou(Piece):
    """ Definit le Fou, deplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super().__init__("Fou", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Fou"""

        tab = [(INFINI, [SANSLIMITE, (1, 1), (1, -1), (-1, 1), (-1, -1)])]

        return (tab, tab)


class Reine(Piece):
    """ Definit la Reine, deplacements autorisés etc... """

    def __init__(self, joueur, terrainOrigine):
        super().__init__("Reine", joueur, terrainOrigine)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible de la Reine"""

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
    :return: deux tableaux, celui des couples déplacements en cas normal et celui des couples déplacements en cas d"ennemi
    """

    def nouveau_terrain(terrainActuel, modification):
        """ Passe d'un terrain à l'autre selon modification. """
        return (terrainActuel + modification) % 3

    def nv_case(u):
        """ Sert à calculer les nouvelles coordonées d'une case lors d'un changement de terrain. """
        return 2 * n - u - 1

    def traite(couplesVecteurs):
        """ Coeur de la procédure."""
        p, d, g = pos
        depsPossibles = []  # contiendra le résultat final de traite

        for typeDep, vecteurs in couplesVecteurs:
            if typeDep == FINI:
                depsFini = []
                for vecteur in vecteurs:
                    x, y = vecteur
                    i, j = d + x, g + y
                    if i >= 0 and j >= 0:
                        if d == g and y == x:  # cas où la pièce est sur la diagonale de la mort
                            if i < n:
                                depsFini.append((p, i, j))

                        elif i < n and j < n:
                            depsFini.append((p, i, j))  # pas de dépassement

                        elif i < n:
                            depsFini.append((nouveau_terrain(p, 1), nv_case(j), i))  # dépassement à gauche

                        elif g + y < n:
                            depsFini.append((nouveau_terrain(p, -1), j, nv_case(i)))  # dépassement à droite

                        else:  # double dépacement
                            # en cas de double dépacement on peut avoir besoin du cas SP pour gérer les situations
                            # au centre
                            if not isinstance(vecteur, SP):  # cas vecteur normal
                                depsFini.append((nouveau_terrain(p, signe(x * y)), nv_case(i), nv_case(j)))
                            else:
                                if (d, g) == (5, 5):  # les vecteurs SP ne s'appliquent qu'au centre du plateau
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
                depsRock = []
                for x, y in vecteurs:
                    depsRock.append((p, d + x, g + y))  # Ici le code est simple car un Rock ne permet pas de changer de terrain

                if depsRock:
                    depsPossibles.append((ROCK, depsRock))

            else:
                raise ValueError("Type de déplacement inconnu.")
        return depsPossibles

    return traite(déplacementsSansEnnemi), traite(déplacementsAvecEnnemi)


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


if __name__ == '__main__':
    # print(test_infini(2, 0, 0, 0, 1))
    print(traduction_en_couples_déplacements(*Tour.deplacements_possibles(2), (0, 0, 0), 6))
