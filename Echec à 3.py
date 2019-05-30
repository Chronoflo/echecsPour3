from constantes import *

# Jeu d'Echec pour 3 joueurs
class ArmesAFeu:
    def __init__(self, nom, munitions, possedeViseur):
        self.nom = nom
        self.munitions = munitions
        self.possede_viseur = possedeViseur

    def tire(self):
        if self.munitions > 0:
            print("Pan !")
        else:
            print("Ma vie est un échec.")


class Pistolet(ArmesAFeu):
    def __init__(self, munitions):
        super().__init__("Piou piou", munitions, False)


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
