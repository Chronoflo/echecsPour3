# Pour l'affichage on utilise la bibliothèque supplémentaire pygame
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
    """ Redimensionne l'image donnée en argument pour qu'elle rentre dans
    la "boîte", sans changer son ratio. """
    bx,by = boite
    ix,iy = img.get_size()
    if ix > iy:
        coeffTaille = bx/float(ix)
        sy = coeffTaille * iy
        if sy > by:
            coeffTaille = by/float(iy)
            sx = coeffTaille * ix
            sy = by
        else:
            sx = bx
    else:
        coeffTaille = by/float(iy)
        sx = coeffTaille * ix
        if sx > bx:
            coeffTaille = bx/float(ix)
            sx = bx
            sy = coeffTaille * iy
        else:
            sy = by
    return pygame.transform.scale(img, (int(sx),int(sy)))

def affichage():
    """C'est la fonction principale de l'affichage.
    Elle appelle les fonctions affichage_pieces, redimensionne et detecte_terrain_curseur.
    Elle s'occupe de créer la fenêtre du jeu et du passage du "menu" au plateau, et coordonne l'affichage de chaque pièce, en interaction avec le joueur."""
    pygame.init()

    listeJoueurs = ListeDeJoueurs(Joueur("Arthur", 0, BLEU), Joueur("Sarah", 1, VERT),
                              Joueur("Florian", 2, ROUGE))
    plateau = Plateau(listeJoueurs)

    fenetre = pygame.display.set_mode((800,600), RESIZABLE)
    # On crée une fenêtre, redimensionnable
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    imagePlateau = pygame.image.load("Image/Plateau - Echecs à 3.png").convert_alpha()
    # Importation d'une image pour remplir la fenêtre, puis de celle du plateau, dont on gère la tranparence.
    pygame.display.set_caption("Echecs à 3")
    # On donne un intitulé à la fenêtre

    fenetre.blit(fond, (0, 0))
    # On "colle" l'image en haut à gauche dans la fenêtre

    bouton1 = pygame.image.load("Image/Commencer 1.png").convert_alpha()
    bouton2 = pygame.image.load("Image/Commencer 2.png").convert_alpha()
    position_bouton = bouton1.get_rect()
    position_bouton = position_bouton.move(200, 300)
    fenetre.blit(bouton1, position_bouton)
    # Affichage de même du bouton qui permettra au joueur de commencer le jeu.

    pygame.display.flip()
    Piece.chargeImages()
    # On charge les images associées à chaque pièce.

    continuer = 1
    accueil = 1
    jeu = 0
    pygame.key.set_repeat(400, 30)
    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
                # Fin du programme si le joueur ferme la fenêtre
            if event.type == VIDEORESIZE:
                pygame.display.set_mode(event.size, RESIZABLE)
                # Réajuste la "zone de dessin" pour permettre le remplissage de toute la fenêtre lorsqu'on la redimensionne

        #BOUCLE MENU:
            pygame.time.Clock().tick(30)
            if accueil:
                if event.type == MOUSEMOTION:
                    fenetre.blit(fond, (0,0))
                    fenetre.blit(bouton1, position_bouton)
                    if position_bouton.collidepoint(pygame.mouse.get_pos()):
                        fenetre.blit(bouton2, position_bouton)
                        # Changement d'image pour le bouton au passage de la souris
                    pygame.display.flip()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if position_bouton.collidepoint(pygame.mouse.get_pos()):
                        # Réaction au clic sur le bouton : sortie de la boucle du menu, entrée dans celle du jeu
                        accueil = 0
                        jeu = 1

        #BOUCLE JEU:
            if jeu:
                fenetre.fill(BLANC)
                hauteurFenetre, largeurFenetre = fenetre.get_rect()[3], fenetre.get_rect()[2]
                # On récupère les dimensions de la fenêtre, et les coordonnées du centre du plateau (qui sera centré dans la fenêtre)
                centre = complex(largeurFenetre/2, hauteurFenetre/2)
                imageRedim = redimensionne(imagePlateau, (largeurFenetre, hauteurFenetre))
                hauteur = imageRedim.get_rect()[3]
                largeur = imageRedim.get_rect()[2]
                # Nouvelles dimensions de l'image du plateau
                xPlateau, yPlateau = (largeurFenetre-largeur)/2, (hauteurFenetre-hauteur)/2
                # Nouvelle position de l'image du plateau
                fenetre.blit(imageRedim, (xPlateau, yPlateau))

                affichage_pieces (plateau, imageRedim, fenetre)

                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    # Le joueur clique dans la fenêtre, peut-être sur le plateau
                    detecte_terrain_curseur(centre, event, largeur, hauteur, xPlateau, yPlateau)
                pygame.display.flip()


def affichage_pieces (plateau, imagePlateau, fenetre):
    """ Cette fonction prend en entrée la matrice des pièces sur le plateau, l'image (aux dimensions de la fenêtre) qui lui est associée ainsi que la fenêtre.
    Elle parcourt cette matrice et affiche pour chaque pièce son image sur la case correspondante, qu'elle atteint par la combinaison linéaire de deux vecteurs du plan """
    hauteur = imagePlateau.get_rect()[3]
    largeur = imagePlateau.get_rect()[2]
    hauteurFenetre, largeurFenetre = fenetre.get_rect()[3], fenetre.get_rect()[2]
    centre = complex(largeurFenetre/2, hauteurFenetre/2)
    u = complex(largeur/12, -hauteur/24)    # selon l'axe d
    v = complex(-largeur/12, -hauteur/24)   # et ici, l'axe g

    for p in range (3) :
        for d in range (6):
            for g in range (6):
                case = plateau[p][d][g]
                if isinstance (case, Piece) : # A faire si une pièce est à l'emplacement de la case
                    image = redimensionne(case.image, (largeur/12, hauteur/12))
                    décaleImage = complex((-image.get_rect()[2])/2, -3*(image.get_rect()[3])/4)
                    centreCase = centre + complex(0, 11*hauteur/24)
                    z = décaleImage + centre + np.exp(2j*p*np.pi/3)*(centreCase + d*u + g*v - centre)
                    # On fait une rotation autour du centre du plateau, d'un tiers de tour ou de deux en fonction du terrain sur lequel se trouve la pièce
                    fenetre.blit(image, (z.real, z.imag))

def detecte_terrain_curseur(centre, event, largeurPlateau, hauteurPlateau, xPlateau, yPlateau):
    """ Cette fonction, grâce à un appel à la fonction detecte_case_curseur, renvoie le triplet de coordonnées de la case sur laquelle le joueur a cliqué.
        Elle s'occupe essentiellement de reconnaître le terrain auquel cette case appartient pour faciliter le repérage des deux autres coordonnées par la fonction auxiliaire appelée. """
    xCurseur = event.pos[0]
    yCurseur = event.pos[1]
    def frontiere01(x): # caractérisation de la droite séparant les terrains 0 et 1
        return 3*hauteurPlateau/4 + yPlateau - (x-xPlateau) * np.tan(np.pi/6)
    def frontiere02(x): # droite servant de frontière entre les terrains 0 et 2
        return hauteurPlateau/4 + yPlateau + (x-xPlateau) * np.tan(np.pi/6)
    # Pas besoin d'en définir une troisième, elle est verticale et est remplacée par un test sur x
    # On définit maintenant les limites obliques de l'hexagone
    def haut1(x):
        return hauteurPlateau / 4 + yPlateau - (x - xPlateau)*np.tan(np.pi / 6)
    def bas1(x):
        return 5*hauteurPlateau / 4 + yPlateau - (x - xPlateau)*np.tan(np.pi / 6)
    def haut2(x):
        return -hauteurPlateau / 4 + yPlateau + (x - xPlateau)*np.tan(np.pi / 6)
    def bas2(x):
        return 3*hauteurPlateau / 4 + yPlateau + (x - xPlateau)*np.tan(np.pi / 6)
    if yCurseur<haut1(xCurseur) or yCurseur<haut2(xCurseur) or yCurseur>bas1(xCurseur) or yCurseur>bas2(xCurseur) or xCurseur<xPlateau or xCurseur>xPlateau+largeurPlateau :
        None # Le curseur est hors du plateau
    elif yCurseur < frontiere01(xCurseur) and xCurseur < (largeurPlateau/2+xPlateau) :
        # Le curseur est sur une case du terrain 1
        detecte_case_curseur(centre, xCurseur, yCurseur, largeurPlateau, hauteurPlateau, xPlateau, yPlateau, 1)
    elif yCurseur > frontiere02(xCurseur) :
        # Le curseur est sur une case du terrain 0
        detecte_case_curseur(centre, xCurseur, yCurseur, largeurPlateau, hauteurPlateau, xPlateau, yPlateau, 0)
    else :
        # Il est dans le terrain 2
        detecte_case_curseur(centre, xCurseur, yCurseur, largeurPlateau, hauteurPlateau, xPlateau, yPlateau, 2)

def detecte_case_curseur (centre, xCurseur, yCurseur, largeurPlateau, hauteurPlateau, xPlateau, yPlateau, p):
    """ Connaissant le terrain où se trouve la case à identifier et les coordonnées du curseur et du centre, avec les mesures et position du plateau, cette fonction renvoie les coordonnées de la case cliquée"""
    if p==0 :
        coordonnées = [p, 5, 5]
        for d in range (5, 0, -1) :
            if yCurseur > ((9-d)*hauteurPlateau)/12 + yPlateau + (xCurseur - xPlateau) * np.tan(np.pi / 6):
                # Le curseur est en dessous de la droite définie ici : on doit descendre vers la case (0,0,0)
                coordonnées[1] = coordonnées[1] - 1
        for g in range (5, 0, -1) :
            if yCurseur > (15-g)*hauteurPlateau/12 + yPlateau - (xCurseur - xPlateau) * np.tan(np.pi / 6):
                coordonnées[2] = coordonnées[2] - 1
    if p==1 : # C'est la même logique, mais il a semblé nécessaire de distinguer les trois cas de terrains, faute de formule permettant de les associer clairement
        coordonnées = [p, 5, 5]
        for d in range (5, 0, -1) :
            if yCurseur < (3+d)*hauteurPlateau/12 + yPlateau - (xCurseur - xPlateau) * np.tan(np.pi / 6) :
                coordonnées[1] = coordonnées[1] - 1
        for g in range (5, 0, -1) :
            if xCurseur < xPlateau +  g*largeurPlateau/12 :
                coordonnées[2] = coordonnées[2] - 1
    if p==2 :
        coordonnées = [p, 5, 5]
        for d in range (5, 0, -1) :
            if xCurseur > largeurPlateau/2+xPlateau+(6-d)*largeurPlateau/12 :
                coordonnées[1] = coordonnées[1] - 1
        for g in range (5, 0, -1) :
            if yCurseur < (g-3)*hauteurPlateau/12 + yPlateau + (xCurseur-xPlateau) * np.tan(np.pi/6):
                coordonnées[2] = coordonnées[2] - 1
    return (tuple(coordonnées))


if __name__ == '__main__':
    affichage()
