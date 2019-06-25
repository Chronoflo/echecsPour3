import random

from kivy.metrics import Metrics


def px_to_m(px):
    """ Renvoie la longueur en m de px pixels. """
    res = 0.0254 * px / Metrics.dpi
    return res


def rand_sign():
    """ Signe aléatoire entre -1 et 1. """
    if random.random() >= 0.5:
        return 1
    else:
        return -1


if __name__ == '__main__':
    print(px_to_m(100))


def signe(x):
    """ Renvoie une information sur le signe de x. """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def concat(tab):
    """ Renvoie la concaténation des éléments de tab. """
    if tab:
        res = type(tab[0])()
        for t in tab:
            res += t
        return res
    else:
        return []


tab_width = 4


def make_tab(txt):
    """ Remplace les tabulations par des espaces. """
    i = 0
    res = ""
    for char in txt:
        if char == '\t':
            res += " " * (tab_width - i)
        else:
            res += char
        i = (i + 1) % tab_width
    return res


def appartient_tableau_de_couples(coords, *tableaux):
    """ Renvoie vrai ssi coords appartient à un des tableaux de déplacements de tableaux. """
    for t in tableaux:
        for typeDép, déps in t:
            for dép in déps:
                if dép == coords:
                    return True
    return False


if __name__ == '__main__':
    print(make_tab("bon\tchien"))
