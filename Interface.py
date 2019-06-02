import pygame
from pygame.locals import *


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





