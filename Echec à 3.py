from constantes import *

# Jeu d'Echec pour 3 joueurs
class ArmesAFeu:
    def __init__(self, nom, munitions, possedeViseur):
        self.nom = nom
        self.munitions = munitions
        self.possede_viseur = possedeViseur

class Pion(Piece):
    """ Definit le pion, deplacements autorisés etc... """
    def __init__(self):
        super().__init__("Pion")

    def deplacementsPossibles(self, emplacementPresent):
        """ Envois le tableau des déplacement possible du Pion.
        Separe le cas où il y a une piece ennemie et où il n'y a rien """

        tabAvecEnnemies = [[emplacementPresent[0],emplacementPresent[1]+1,
                        emplacementPresent[2]+1],
                        [emplacementPresent[0],emplacementPresent[1]+1,
                        emplacementPresent[2]-1],
                        [emplacementPresent[0],emplacementPresent[1]-1,
                        emplacementPresent[2]+1]]


class ListesDeJoueur:
    def __init__(self):
        self.joueurs = [J1, J2, J3]
        self.iJoueurActuel = 0

    def joueur_suivant(self):
        if self.iJoueurActuel + 1 < len(self.joueurs):
            self.iJoueurActuel += 1
        else:
            self.iJoueurActuel = 0

        return self.joueurs[self.iJoueurActuel]

    def enleve_joueur(self, joueur):
        try:
            iJoueurAEnlever = self.joueurs.index(joueur)
        except ValueError:
            print("Ce joueur ne joue pas.")
            return None
        else:
            if iJoueurAEnlever <= self.iJoueurActuel:
                self.iJoueurActuel -= 1
            del self.joueurs[iJoueurAEnlever]

def initialisation_plateau():
    t=[[[Roi],  [Tour2],    [Fou2],     [Pion7],[None],[None]],
       [[Fou1], [Reine],    [Cavalier2],[Pion6],[None],[None]]
       [[Tour1],[Cavalier1],[Chèvre],   [Pion5],[None],[None]]
       [[Pion1],[Pion2],    [Pion3],    [Pion4],[None],[None]]
       [[None], [None],     [None],     [None], [None],[None]]
       [[None], [None],     [None],     [None], [None],[None]]]
    return [t for i in range(3)]
