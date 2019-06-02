from fonctions import signe
def f(i, j):
    """
    Ajoute les coordonnées corrigées d'une case à un tableau.
    :param id: identifiant du déplacement
    :param i et j: coordonnées non corrigées
    :param t: tableau auquel ajouter la case corrigée
    """
    if d == g and y == x:
        # Cas où la pièce est sur la diagonale de la mort
        if 0 <= i < n:
            return p, i, j
    elif i < n and j < n:
        # Cas où la pièce ne change pas de terrain
        return p, i, j
    elif i < n:
        return nouveau_terrain(p, 1), nv_case(j), i
    elif g + y < n:
        return nouveau_terrain(p, -1), j, nv_case(i)
    else:
        return nouveau_terrain(p, signe(x*y)), nv_case(i), nv_case(j)

def nouveau_terrain(terrainActuel, modification):
    return (terrainActuel + modification) % 3

def nv_case(u):
    return 2*n - (u+1)


n = 6
p, d, g = 2, 5, 5
x, y = 2, 1
print(f(d + x, g+y))
