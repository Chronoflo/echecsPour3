# Jeu d'Echec pour 3 joueurs
class ArmesAFeu:
    def __init__(self, nom, munitions, possede_viseur):
        self.nom = nom
        self.munitions = munitions
        self.possede_viseur = possede_viseur

    def tire(self):
        if self.munitions > 0:
            print("Pan !")
        else:
            print("Ma vie est un échec.")


class Pistolet(ArmesAFeu):
    def __init__(self, munitions):
        super().__init__("Piou piou", munitions, False)
