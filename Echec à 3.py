from plateau import Plateau
from Pieces import Piece
from joueur import Joueur, ListesDeJoueur
import pygame
from pygame.locals import *
from numpy import exp, pi, sqrt
from Interface import ROUGE, VERT, BLEU


def dessine_composants(surface, plateau):
    """ Affiche tous les composants du plateau. """
    def cercle(col, pos, radius=2):
        pygame.draw.circle(surface, col, pos, radius)

    center = complex(400, 400)  # Centre du plateau
    c = 30  # Taille de la diagonale la plus courte d'une case
    cercle(VERT, (int(center.real), int(center.imag)), 8)
    for p in range(3):
        origine = (center + c * 6 * exp((pi/2 + 2*p*pi/3) * 1j))  # Point (0,0) pour le terrain p
        for d in range(6):
            for g in range(6):
                if isinstance(plateau[p][d][g], Piece):
                    # Calcule la position d'une pièce
                    z = origine - c*((d - g) * (sqrt(3)/2) + (1 + d + g) * 1j/2) * exp(p*2j*pi/3)
                    # Affiche la pièce
                    image = plateau[p][d][g].image
                    x, y, w, h = image.get_rect()
                    surface.blit(plateau[p][d][g].image, (z.real - w/2, z.imag - h/2))


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
