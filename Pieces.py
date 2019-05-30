# Jeu d'Echec pour 3 joueurs

class Piece:
    """ Définit la classe piece, qui définira le comportement général de chaque
    pieces (pions, tours, dame, ...)
    Nom € { pion, dame, tour, ... } """
    def __init__(self, nom):
        self.nom = nom
        self.emplacementInitial = True

class Pion(Piece):
    """ Definit le pion, deplacements autorisés etc... """
    def __init__(self):
        super().__init__("Pion")

    def deplacementsPossibles(self, emplacementPresent):
        """ Envois un Booléen devant qui dit si le déplacement est infini ou
        fini, le tableau des déplacements fini (vecteur des déplacements
        infinis) possible du Pion.
        Separe le cas où il y a une piece ennemie et où il n'y a rien.
        Avec à la fin le max des déplacements possibles si déplacement infini"""
#
        """tabAvecEnnemies = [[emplacementPresent[0],emplacementPresent[1]+1,
                        emplacementPresent[2]+1],
                        [emplacementPresent[0],emplacementPresent[1]+1,
                        emplacementPresent[2]-1],
                        [emplacementPresent[0],emplacementPresent[1]-1,
                        emplacementPresent[2]+1]]

        if self.emplacementInitial:
            tabSansEnnemies = [[emplacementPresent[0],emplacementPresent[1]+1,
                        emplacementPresent[2]],
                        [emplacementPresent[0],emplacementPresent[1],
                        emplacementPresent[2]+1]
                        [emplacementPresent[0],emplacementPresent[1]+2,
                        emplacementPresent[2]]
                        [emplacementPresent[0],emplacementPresent[1],
                        emplacementPresent[2]+2]]

        else:
            tabSansEnnemies = [[emplacementPresent[0],emplacementPresent[1]+1,
                        emplacementPresent[2]],
                        [emplacementPresent[0],emplacementPresent[1],
                        emplacementPresent[2]+1]]

        return (False, tabAvecEnnemies, tabSansEnnemies)"""

class Roi(Piece):
    """ Definit le Roi, deplacements autorisés etc... """
    def __init__(self):
        super().__init__("Roi")

    def deplacementsPossibles(self, emplacementPresent):
        """ Envois le tableau des déplacement possible du Roi
        Avec un Booléen devant qui dit si le déplacement est infini ou fini """
#
        """tab = [[emplacementPresent[0],emplacementPresent[1]+1,
                   emplacementPresent[2]],
               [emplacementPresent[0],emplacementPresent[1],
                   emplacementPresent[2]+1]
               [emplacementPresent[0],emplacementPresent[1]-1,
                   emplacementPresent[2]]
               [emplacementPresent[0],emplacementPresent[1],
                   emplacementPresent[2]-1]
               [emplacementPresent[0],emplacementPresent[1]+1,
                   emplacementPresent[2]]+1,
               [emplacementPresent[0],emplacementPresent[1]-1,
                   emplacementPresent[2]+1]
               [emplacementPresent[0],emplacementPresent[1]+1,
                   emplacementPresent[2]-1]
               [emplacementPresent[0],emplacementPresent[1]-1,
                   emplacementPresent[2]-1]]

    return (False, tab, tab)"""

class Cavalier(Piece):
    """ Definit le Roi, deplacements autorisés etc... """
    def __init__(self):
        super().__init__("Cavalier")

    def deplacementsPossibles(self, emplacementPresent):
        """ Envois le tableau des déplacement possible de la Cavalier """




