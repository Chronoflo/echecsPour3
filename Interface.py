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


ROUGE = SuperColor("rouge", (255,   0,   0))
VERT = SuperColor("vert", (0, 255,   0))
BLEU = SuperColor("bleu", (0,   0, 255))
BLANC = SuperColor("blanc", (255, 255, 255))
NOIR = SuperColor("noir", (0, 0, 0))

def redimensionne(img, boite):
    """ Scales 'img' to fit into box bx/by.
     This method will retain the original image's aspect ratio """
    bx,by = boite
    ix,iy = img.get_size()
    if ix > iy:
        # fit to width
        scale_factor = bx/float(ix)
        sy = scale_factor * iy
        if sy > by:
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            sy = by
        else:
            sx = bx
    else:
        # fit to height
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        if sx > bx:
            scale_factor = bx/float(ix)
            sx = bx
            sy = scale_factor * iy
        else:
            sy = by
    return pygame.transform.scale(img, (int(sx),int(sy)))

def affichage():
    pygame.init()

    listeJoueurs = ListeDeJoueurs(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT),
                              Joueur("Florian", 2, ROUGE))
    plateau = Plateau(listeJoueurs)

    fenetre = pygame.display.set_mode((800,600), RESIZABLE)
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    pygame.display.set_caption("Coucou Sarah :p")
    terrainBleu = pygame.image.load("Image/Plateau - Echecs à 3.png").convert_alpha()
    terrainVert = pygame.image.load("Image/Plateau - Echecs à 3.png").convert_alpha()
    terrainRouge = pygame.image.load("Image/Plateau - Echecs à 3.png").convert_alpha()
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
            if event.type == VIDEORESIZE:
                pygame.display.set_mode(event.size, RESIZABLE)
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
                fenetre.fill(BLANC)
                hauteurFenetre, largeurFenetre = fenetre.get_rect()[3], fenetre.get_rect()[2]
                imageRedim = redimensionne(listeTerrains[j], (largeurFenetre, hauteurFenetre))
                hauteur = imageRedim.get_rect()[3]
                largeur = imageRedim.get_rect()[2]
                xPlateau, yPlateau = (largeurFenetre-largeur)/2, (hauteurFenetre-hauteur)/2
                fenetre.blit(imageRedim, (xPlateau, yPlateau))
                affichage_pièces (plateau, imageRedim, fenetre)
                if event.type == KEYDOWN:
                    j=(j+1)%3
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    detecteCaseCurseur(event, largeur, hauteur, xPlateau, yPlateau)
                pygame.display.flip()


def affichage_pièces (plateau, imagePlateau, fenetre):
    def cercle(pos, r=8):
        a, b = pos
        pygame.draw.circle(fenetre, VERT, (int(a), int(b)), r)

    hauteur = imagePlateau.get_rect()[3]
    largeur = imagePlateau.get_rect()[2]
    hauteurFenetre, largeurFenetre = fenetre.get_rect()[3], fenetre.get_rect()[2]
    centre = complex(largeurFenetre/2, hauteurFenetre/2)
    Image = redimensionne(pygame.image.load("Image/Pieces/bleu_Pion00.png").convert_alpha(), (largeur/8, hauteur/8))
    u = complex(largeur/12, -hauteur/24) # selon l'axe d
    v = complex(-largeur/12, -hauteur/24)# attention l'axe est vers le bas

    for p in range (3) :
        for d in range (6):
            for g in range (6):
                case = plateau[p][d][g]
                if isinstance (case, Piece) :
                    décaleImage = complex((-Image.get_rect()[2])/2, -(Image.get_rect()[3])/2)
                    centreCase = centre + complex(0, 11*hauteur/24)
                    z = décaleImage + centre + np.exp(2j*p*np.pi/3)*(centreCase + d*u + g*v - centre)
                    fenetre.blit(Image, (z.real, z.imag))

def detecteCaseCurseur(event, largeurPlateau, hauteurPlateau, xPlateau, yPlateau):
        xCurseur = event.pos[0]
        yCurseur = event.pos[1]
        def frontiere01(x):
            return 3*hauteurPlateau/4 - x * (x*np.tan(np.pi/6))
        def frontiere02(x):
            return hauteurPlateau/4 + x * (x*tan(np.pi/6))
        if yCurseur < frontiere01(xCurseur) and xCurseur < (largeurPlateau+xPlateau)/2 :
            print ("terrain 1")



if __name__ == '__main__':
    affichage()
