from constantes import INFINI
from plateau import Plateau
from Pieces import Piece, traduction_en_couples_déplacements, Cavalier, Roi, Tour, Fou, Pion, Chevre, Reine, dep_effectifs
from joueur import Joueur, ListesDeJoueur
import pygame
from pygame.locals import *
from numpy import exp, pi, sqrt
from Interface import ROUGE, VERT, BLEU, BLANC


def dessine_composants():
    pass



if __name__ == '__main__':
    listeJoueurs = ListesDeJoueur(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT),
                                  Joueur("Florian", 2, ROUGE))
    plateau = Plateau(listeJoueurs)

    pygame.init()

    fenetre = pygame.display.set_mode((800, 600), RESIZABLE)
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    centrePlateau = (400, 400)

    fenetre.blit(fond, (0, 0))
    pos = (0,0,0)
    piece = Roi(Joueur("Moi", 0, ROUGE), 0)
    piece.emplacementInitial = True
    piece.terrainActuel = pos[0]
    pygame.display.flip()
    continuer = 1
    print(plateau[0][2][0])

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
