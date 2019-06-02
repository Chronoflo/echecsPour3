from constantes import *
from plateau import Plateau
from joueur import Joueur, ListesDeJoueur
import pygame
from pygame.locals import *
from Interface import dessine_composants

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)


if __name__ == '__main__':
    listeJoueurs = ListesDeJoueur(Joueur("Arthur", 0, BLUE), Joueur("Sarah", 1, GREEN),
                                  Joueur("Florian", 2, RED))
    plateau = Plateau(listeJoueurs)

    pygame.init()

    fenetre = pygame.display.set_mode((800, 600))
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    fenetre.blit(fond, (0, 0))
    dessine_composants(fenetre, plateau)
    pygame.display.flip()
    continuer = 1

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
