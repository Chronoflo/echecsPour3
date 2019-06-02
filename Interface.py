from math import sqrt, pi
from numpy import exp

import pygame
from pygame.locals import *
from Pieces import Piece

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

def dessine_composants(surface, plateau):
    def cercle(col, pos, radius=2):
        pygame.draw.circle(surface, col, pos, radius)
    center = complex(400, 300)
    cercle(GREEN, (400,300), 8)
    c = 30
    for p in range(3):
        for d in range(6):
            for g in range(6):
                origine = (center + c * 6 * exp((pi / 2 + 2 * i * pi / 3) * 1j))

                if isinstance(plateau[p][d][g], Piece):
                    piece = plateau[p][d][g]
                    z = origine - c*((d - g) * (sqrt(3)/2) + (1 + d + g) * 1j/2)
                    pygame.draw.circle(surface, piece.joueur.couleur,
                                       (int(z.real), int(z.imag)), 2)

def affichage():
    pygame.init()

    fenetre = pygame.display.set_mode((800,600))
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    pygame.display.set_caption("Coucou Sarah :p")
    joueurBleu = pygame.image.load("Image/Plateau joueur Bleu.jpg").convert()
    joueurVert = pygame.image.load("Image/Plateau joueur Vert.jpg").convert()
    joueurRouge = pygame.image.load("Image/Plateau joueur Rouge.jpg").convert()
    listeJoueurs = [joueurBleu, joueurRouge, joueurVert]
    fenetre.blit(fond, (0, 0))

    bouton1 = pygame.image.load("Image/Commencer 1.png").convert_alpha()
    bouton2 = pygame.image.load("Image/Commencer 2.png").convert_alpha()
    position_bouton = bouton1.get_rect()
    position_bouton = position_bouton.move(200, 300)


    fenetre.blit(bouton1, position_bouton)

    pygame.display.flip()

    continuer = 1
    accueil = 1
    jeu = 0
    pygame.key.set_repeat(400, 30)
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
        #BOUCLE MENU:
            pygame.time.Clock().tick(30)
            if accueil:
                if event.type == MOUSEMOTION:
                    fenetre.blit(fond, (0,0))
                    fenetre.blit(bouton1, position_bouton)
                    if position_bouton.collidepoint(pygame.mouse.get_pos()):
                        fenetre.blit(bouton2, position_bouton)
                    pygame.display.flip()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if position_bouton.collidepoint(pygame.mouse.get_pos()):
                        accueil = 0
                        jeu = 1
                        j = 0
        #BOUCLE JEU:
            if jeu:
                fenetre.blit(listeJoueurs[j], (0,0))
                if event.type == KEYDOWN:
                    j=(j+1)%3
            #fenetre.blit(joueurRouge, (0,0))
            pygame.display.flip()


if __name__ == '__main__':
    affichage()





