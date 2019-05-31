# Jeu d'Echec pour 3 joueurs

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

        tabAvecEnnemis = 0, [ (1,1), (-1,1), (1,-1) ]
        """ La régle de la prise en passant n'est pas présente dans cette
        version """

        if self.emplacementInitial:
            tabSansEnnemis = 1 , [ (1,0), (0,1) ], 2

        else:
            tabSansEnnemis = 0 , [ (1,0), (0,1) ]

        return (tabSansEnnemis, tabAvecEnnemis)

class Roi(Piece):
    """ Definit le Roi, deplacements autorisés etc... """
    def __init__(self, joueur):
        super().__init__("Roi", joueur)

    def deplacements_possibles(self):
        """ Envois le tableau des déplacement possible du Roi
        Avec la possiblilité de rock"""

        tabSansEnnemis = (0 , [(0,1),(1,0),(-1,0),(0,-1), (1,1),(1,-1),
                            (-1,1),(-1,-1)] ), (2 , [(2,0), (1,0)] )

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

"""def fonction_auxiliaire_de_la_mort(tabssE,tabacE,pos):
    ns = len(tabssE[1])
    na = len(tabacE[1])


    for i in range(ns)"""