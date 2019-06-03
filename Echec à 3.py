from plateau import Plateau
from Pieces import Piece
from joueur import Joueur, ListesDeJoueur
import pygame
from pygame.locals import *
from numpy import exp, pi, sqrt
from Interface import ROUGE, VERT, BLEU, dessine_composants


if __name__ == '__main__':
    listeJoueurs = ListesDeJoueur(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT),
                                  Joueur("Florian", 2, ROUGE))
    plateau = Plateau(listeJoueurs)

    pygame.init()

    fenetre = pygame.display.set_mode((800, 600))
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    Piece.charge_images()

    fenetre.blit(fond, (0, 0))
    dessine_composants(fenetre, plateau)
    pygame.display.flip()
    continuer = 1

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
