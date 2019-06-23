# Pour l'affichage on utilise la bibliothèque supplémentaire pygame
import pygame
from pygame.locals import *

import numpy as np

from constantes import SELECTION_PIECE, VALIDATION_DEPLACEMENT
from fonctions import appartient_tableau_de_couples
from plateau import Plateau
from Pieces import Piece
from joueur import Joueur, ListeDeJoueurs


class SuperColor(pygame.Color):
    """ Une couleur pygame dotée d'un nom. """
    def __init__(self, nom, couleur):
        super().__init__(*couleur)
        self.nom = nom


class ImagePlateau:
    def __init__(self, terrainEnBas):
        self.terrainEnBas = terrainEnBas
        plateauJoueurRouge = pygame.image.load("Image/plateau_joueur_rouge.png").convert_alpha()
        plateauJoueurVert = pygame.image.load("Image/plateau_joueur_vert.png").convert_alpha()
        plateauJoueurBleu = pygame.image.load("Image/plateau_joueur_bleu.png").convert_alpha()
        self.listePlateaux = [plateauJoueurRouge, plateauJoueurVert, plateauJoueurBleu]
        self.surface = self.listePlateaux[self.terrainEnBas]

    def joueur_suivant(self):
        """ Utiliser en multijoueur sur un même ordi. """
        self.terrainEnBas = (self.terrainEnBas - 1) % 3
        self.surface = self.listePlateaux[self.terrainEnBas]



ROUGE = SuperColor("rouge", (255,   0,   0))
VERT = SuperColor("vert", (0, 255,   0))
BLEU = SuperColor("bleu", (0,   0, 255))
BLANC = SuperColor("blanc", (255, 255, 255))
NOIR = SuperColor("noir", (0, 0, 0))
JAUNE_SYMPA = SuperColor("jaune sympa", (200,200,0))
ROUGE_MECHANT = SuperColor("rouge méchant", (170,0,0))


def dessine_cases(surface_plateau: pygame.Surface, déplacements: list, terrainEnBas, color_=JAUNE_SYMPA):
    def cercle(col, pos, radius=2):
        pygame.draw.circle(surface_plateau, col, pos, radius)
    x, y, w, h = surface_plateau.get_rect()
    centre = complex(w / 2, h / 2)  # Centre du plateau
    c = surface_plateau.get_height() / 12  # Taille de la diagonale la plus courte d'une case
    # cercle(VERT, (int(centre.real), int(centre.imag)), 200)

    for typeDép, cases in déplacements:
        # print(cases)
        for p, d, g in cases:
            origine = (centre + c * 6 * np.exp((np.pi / 2 + 2 * ((p - terrainEnBas) % 3) * np.pi / 3) * 1j))  # Point (0,0) pour le terrain p
            z = origine + c * ((d - g) * (np.sqrt(3) / 2) - (1 + d + g) * 1j / 2) * np.exp(((p - terrainEnBas) % 3) * 2j * np.pi / 3)
            cercle(color_, (int(z.real), int(z.imag)), 5)


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


def affichage(nom_joueur, joueur_0, joueur_1, joueur_2, sur_déplacement_pièce=None, sur_attente_autres_joueurs=None):
    """C'est la fonction principale de l'affichage.
    Elle appelle les fonctions affichage_pieces, redimensionne et detecte_terrain_curseur.
    Elle s'occupe de créer la fenêtre du jeu et du passage du "menu" au plateau, et coordonne l'affichage de chaque pièce, en interaction avec le joueur."""
    pygame.init()
    listeJoueurs = ListeDeJoueurs(Joueur(joueur_0, 0, ROUGE), Joueur(joueur_1, 1, VERT), Joueur(joueur_2, 2, BLEU))
    plateau = Plateau(listeJoueurs)

    def est_tour_du_joueur():
        return nom_joueur == listeJoueurs.joueur_actuel().nom

    fenetre = pygame.display.set_mode((800,600), RESIZABLE)
    # On crée une fenêtre, redimensionnable
    fond = pygame.image.load("Image/Menu 1.jpg").convert()
    # Importation d'une image pour remplir la fenêtre, puis de celle du plateau, dont on gère la tranparence.
    pygame.display.set_caption("Echecs à 3")
    # On donne un intitulé à la fenêtre

    imagePlateau = ImagePlateau([joueur_0, joueur_1, joueur_2].index(nom_joueur))
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
    video_update = False
    jeu = 0
    etape_jeu = SELECTION_PIECE
    pygame.key.set_repeat(400, 30)

    while continuer:
        for event in pygame.event.get():
            if event.type == QUIT:
                continuer = 0
                # Fin du programme si le joueur ferme la fenêtre
            if event.type == VIDEORESIZE:
                pygame.display.set_mode(event.size, RESIZABLE)
                # Réajuste la "zone de dessin" pour permettre le remplissage de toute la fenêtre lorsqu'on la redimensionne
                video_update = True

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
                        video_update = True

            #BOUCLE JEU:
            if jeu:
                if video_update:
                    fenetre.fill(BLANC)
                    hauteurFenetre, largeurFenetre = fenetre.get_rect()[3], fenetre.get_rect()[2]
                    centre = complex(largeurFenetre/2, hauteurFenetre/2)
                    imageRedim = redimensionne(imagePlateau.surface, (largeurFenetre, hauteurFenetre))
                    hauteur = imageRedim.get_rect()[3]
                    largeur = imageRedim.get_rect()[2]
                    xPlateau, yPlateau = (largeurFenetre-largeur)/2, (hauteurFenetre-hauteur)/2
                    fenetre.blit(imageRedim, (xPlateau, yPlateau))
                    affichage_pièces(plateau, imageRedim, fenetre, imagePlateau.terrainEnBas)
                    video_update = False

                if est_tour_du_joueur():
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        pos = detecte_terrain_curseur(centre, event, largeur, hauteur, xPlateau, yPlateau,
                                                imagePlateau.terrainEnBas)
                        if pos is not None:
                            p, d, g = pos
                            case_ciblée = plateau[p][d][g]

                            if etape_jeu == SELECTION_PIECE:
                                if isinstance(case_ciblée, Piece):
                                    pos_piece = pos
                                    piece = case_ciblée
                                    if piece.joueur.nom == nom_joueur:
                                        tb_normal, tb_ennemi = piece.déplacements_possibles(pos, plateau)
                                        dessine_cases(fenetre, tb_normal, imagePlateau.terrainEnBas, JAUNE_SYMPA)
                                        dessine_cases(fenetre, tb_ennemi, imagePlateau.terrainEnBas, ROUGE_MECHANT)
                                        etape_jeu = VALIDATION_DEPLACEMENT
                            elif etape_jeu == VALIDATION_DEPLACEMENT:
                                if appartient_tableau_de_couples(pos, tb_normal, tb_ennemi):
                                    plateau.sur_déplacement_validé(pos_piece, pos)
                                    video_update = True
                                    etape_jeu = SELECTION_PIECE
                                    if sur_déplacement_pièce is not None:
                                        sur_déplacement_pièce(pos_piece, pos)
                                    listeJoueurs.joueur_suivant()
                                elif not isinstance(case_ciblée, Piece):
                                    video_update = True
                                    etape_jeu = SELECTION_PIECE
                                elif case_ciblée.joueur.nom == nom_joueur:
                                    pos_piece = pos
                                    fenetre.blit(imageRedim, (xPlateau, yPlateau))
                                    affichage_pièces(plateau, imageRedim, fenetre, imagePlateau.terrainEnBas)
                                    tb_normal, tb_ennemi = case_ciblée.déplacements_possibles(pos, plateau)
                                    dessine_cases(fenetre, tb_normal, imagePlateau.terrainEnBas, JAUNE_SYMPA)
                                    dessine_cases(fenetre, tb_ennemi, imagePlateau.terrainEnBas, ROUGE_MECHANT)
                else:
                    if sur_attente_autres_joueurs is not None:
                        sur_attente_autres_joueurs(plateau, listeJoueurs)
                    video_update = True
                pygame.display.flip()
        pygame.time.wait(100)

    pygame.quit()

def affichage_pièces (plateau, imagePlateau, fenetre, terrainEnBas):
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
                    z = décaleImage + centre + np.exp(2j*((p - terrainEnBas) % 3) *np.pi/3)*(centreCase + d*u + g*v - centre)
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

def detecte_case_curseur (centre, xCurseur, yCurseur, largeurPlateau, hauteurPlateau, xPlateau, yPlateau, p, terrainEnBas):
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
    coordonnées = (coordonnées[0] + terrainEnBas) % 3, coordonnées[1], coordonnées[2]
    return tuple(coordonnées)


if __name__ == '__main__':
    affichage("Florian", "Florian", "Sarah", "Arthur")
