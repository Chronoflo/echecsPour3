import pygame
from pygame.locals import *

import numpy as np
from plateau import Plateau
from Pieces import Piece
from joueur import Joueur, ListeDeJoueurs


class SuperColor(pygame.Color):
    """ Une couleur pygame dotée d'un nom. """
    def __init__(self, nom, couleur):
        super().__init__(*couleur)
        self.nom = nom


##390,556

ROUGE = SuperColor("rouge", (255,   0,   0))
VERT = SuperColor("vert", (0, 255,   0))
BLEU = SuperColor("bleu", (0,   0, 255))
BLANC = SuperColor("blanc", (255, 255, 255))
NOIR = SuperColor("noir", (0, 0, 0))

def affichage():
    pygame.init()

    listeJoueurs = ListeDeJoueurs(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT),
                              Joueur("Florian", 2, ROUGE))
    plateau = Plateau(listeJoueurs)

    fenetre = pygame.display.set_mode((800,600))
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    pygame.display.set_caption("Coucou Sarah :p")
    terrainBleu = pygame.image.load("Image/Plateau joueur Bleu.jpg").convert()
    terrainVert = pygame.image.load("Image/Plateau joueur Vert.jpg").convert()
    terrainRouge = pygame.image.load("Image/Plateau joueur Rouge.jpg").convert()
    listeTerrains = [terrainBleu, terrainRouge, terrainVert]

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
                fenetre.blit(listeTerrains[j], (0,0))
                affichage_pièces (plateau, listeTerrains[j], fenetre)
                if event.type == KEYDOWN:
                    j=(j+1)%3
            #fenetre.blit(joueurRouge, (0,0))
            pygame.display.flip()



def affichage_pièces (plateau, imagePlateau, fenetre):
    def cercle(pos, r=8):
        a, b = pos
        pygame.draw.circle(fenetre, VERT, (int(a), int(b)), r)

    hauteur = imagePlateau.get_rect()[3]
    largeur = imagePlateau.get_rect()[2]
    centre = complex(largeur/2, hauteur/2)

    Image = pygame.image.load("Image/Pieces/rouge_Cavalier.png").convert_alpha()
    u = complex(largeur/12, 0)
    v = complex(0, hauteur/12)
    for p in range (3) :
        for d in range (6):
            for g in range (6):
                case = plateau[p][d][g]
                if isinstance (case, Piece) :
                    z = np.exp(2j*p*np.pi/3)*(centre +  + (5-d)*u + (5-g)*v)
                    #fenetre.blit(Image, (z.real, z.imag))
                    cercle((z.real, z.imag))
if __name__ == '__main__':
    affichage()