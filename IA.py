
from Piece import CaseVide

def evaluation(jeu):
    """
    Parcours toute les cases, si piece on multiplie par 10 et on ajoute le nombre de coup possible
    Apres min / max
    Entree :
        - jeu : tableau d'entrée (à voir si on rentre class Echiquier / E.echiquier) actuellement je suis parti sur juste l'echiquier
        - joueur : La couleur du joueur (INACTIF)
    """
    score_blanc = 0
    score_noir = 0
    for i in jeu.echiquier:
        for j in i:
            if j.valeur > 0:
                score_blanc += j.valeur * 10 + len(j.coup_possible(jeu)) #Score négatif
            elif j.valeur < 0:
                score_noir += j.valeur * 10 - len(j.coup_possible(jeu))

    return score_blanc + score_noir


def coup_possible(jeu, joueur):
    """Calcule tout les coups possible pour un joueur """
    possibilite={}
    for ligne in range(len(jeu.echiquier)):
        for colonne in range(len(jeu.echiquier[ligne])):
            if jeu.echiquier[ligne][colonne].couleur == joueur:#Voir comment définir joueur ducoup
                possibilite[(ligne, colonne)] = jeu.echiquier[ligne][colonne].coup_possible(jeu)

    return possibilite

def joue_coup(jeu, entree, sortie):
    """ Joue un coup donnée
    entree : La coordonne de départ
    sortie :
        - "mange", piecemangé
        - "promotion", None
        - None, None
    """
    #ATTENTION : NE PAS UTILISER les methodes .avancer() sinon problèmes de récursivité
    #On vérifie si on mange une pièce, si oui on renvoie True et la piece
    if jeu.echiquier[sortie[0]][sortie[1]].valeur != 0:
        x = jeu.echiquier[sortie[0]][sortie[1]]
        jeu.echiquier[entree[0]][entree[1]], jeu.echiquier[sortie[0]][sortie[1]] = CaseVide((entree[0], entree[1])), jeu.echiquier[entree[0]][entree[1]]
        return "mange", x

    elif -1<jeu.echiquier[entree[0]][entree[1]].valeur < 1 and sortie[0] in [0, 7]: #SI la piece est un pion et qu'elle arrive au bout
        jeu.echiquier[entree[0]][entree[1]], jeu.echiquier[sortie[0]][sortie[1]] = CaseVide((entree[0], entree[1])), Dame(jeu.echiquier[entree[0]][entree[1]].couleur, (sortie[0], sortie[1]))
        return "promotion", None

    jeu.echiquier[entree[0]][entree[1]], jeu.echiquier[sortie[0]][sortie[1]] = CaseVide((entree[0], entree[1])), jeu.echiquier[entree[0]][entree[1]]
    return None, None

def annule_coup(jeu, entree , sortie, specialmouv, piece):
    """annule le coup de joue_coup
    Va falloir forcer en rentrant en dur je pense

    entree : arriver
    sortie : depart

    specialmouv : str pour savoir si un mouvement spécial tel que promotion ou mange a eu lieu
    piece : la pièce qui à été mangé
    """
    #SI une pièce a été mangé on la remet
    if specialmouv == "mange":
        pion = jeu.echiquier[sortie[0]][sortie[1]]
        pion.position = (entree[0], entree[1])
        jeu.echiquier[sortie[0]][sortie[1]], jeu.echiquier[entree[0]][entree[1]]= piece, pion
    elif specialmouv == "promotion":
        pion = Pion(jeu.echiquier[sortie[0]][sortie[1]].couleur , (entree[0], entree[1]), False)
        jeu.echiquier[sortie[0]][sortie[1]], jeu.echiquier[entree[0]][entree[1]] = CaseVide((sortie[0], sortie[1])), pion
    else: #Sinon on replace normalement
        pion = jeu.echiquier[sortie[0]][sortie[1]]
        pion.position = (entree[0], entree[1])
        jeu.echiquier[sortie[0]][sortie[1]], jeu.echiquier[entree[0]][entree[1]] = CaseVide((sortie[0],sortie[1])), pion




def min_max(jeu, profondeur, joueur, max = True):
    """
    Fonction pour l'implémentation de l'algorithme minmax
    Entree :
        - jeu : l'échiquier
        - profondeur : profondeur de recherche
        - joueur : couleur du joueur
        - max(imisation) : booléen, True si l'IA joue
    Sortie :

    """
    if joueur == "blanc": #Pour permettre à l'IA de jouer les blanc et les noirsmin_max
        next_joueur = "noir"
    else:
        next_joueur = "blanc"

    
    pat = jeu.pat()
    if profondeur == 0 or pat:
        return evaluation(jeu)
    elif jeu.echec_et_mat(pat, joueur): #Si echec et mat et que c'est le joueur qui joue
        print("Echec et math", joueur , max)
        return 1000
    elif jeu.echec_et_mat(pat, next_joueur): #Si echec et mat et que c'est l'IA qui joue (on vient d'inverser joueur avec next_joueur )
        print("Echec et mat", joueur, max)
        return -1000

    if max == True:
        max_evaluation = -1000000000 #Forcement une vlauer plus grande
        for entree, coup in coup_possible(jeu, joueur).items():
            #coup_possible = {entree : [sortie1, sortie 2 ...], entree2 : [...]}
            for sortie in coup:
                coup_special, piece = joue_coup(jeu, entree, sortie)
                eval = min_max(jeu, profondeur - 1, next_joueur, False)
                annule_coup(jeu, entree, sortie, coup_special, piece)
                if max_evaluation < eval: #Max
                    max_evaluation = eval
        return max_evaluation

    else:

        min_evaluation = 1000000000 #Forcement une valeur plus petite
        for entree, coup in coup_possible(jeu, joueur).items():
            for sortie in coup:
                coup_special, piece = joue_coup(jeu, entree, sortie)
                eval = min_max(jeu, profondeur - 1, next_joueur, True)
                annule_coup(jeu, entree, sortie, coup_special, piece)
                if min_evaluation > eval: #Min
                    min_evaluation = eval
        return min_evaluation


def meilleur_coups(jeu, profondeur, joueur):
    """
    Fonction pour trouver le meilleur coup
    Entree :
    - jeu : l'echiquier
    - profondeur : profondeur de recherche
    - joueur : couleur du joueur
    Sortie :
    - le meilleur coup : tuple (entree, sortie)
    """
    meilleur_coup = None
    max_evaluation = float("-inf")
    for entree, coup in coup_possible(jeu, joueur).items():
        for sortie in coup:
            coup_special, piece = joue_coup(jeu, entree, sortie)
            evaluation = min_max(jeu, profondeur - 1, joueur, False) #On  inverse la couleur du joueur dans min_max
            annule_coup(jeu, entree, sortie, coup_special, piece)
            if max_evaluation < evaluation:
                max_evaluation = evaluation
                meilleur_coup = (entree, sortie)
    return meilleur_coup

#Partie test
if "__main__" == __name__:
    from Piece import *

    class Echiquier:
        """
        Echiquier :
            - echiquier : matrice représentant le plateau, les pièces sont représentées par leur object
            -__repr__ : renvoie l'echiquier dans l'IDE

            -pionToDame : permet de passer un pion en Dame(on pourra demander à l'utilisateur) (INACTIF)
        """
        def __init__(self):
            self.echiquier = [[CaseVide((0,i))for i in range(8)],
                            [CaseVide((1,i))for i in range(8)],
                            [CaseVide((2,i))for i in range(8)],
                            [CaseVide((3,0)), Cavalier("noir", (3,1)), CaseVide((3,2)), CaseVide((3,3)), CaseVide((3,4)), CaseVide((3,5)),CaseVide((3,6)), CaseVide((3,7))],
                            [CaseVide((4,i))for i in range(8)],
                            [Pion("blanc", (5,0)),CaseVide((5,1)), CaseVide((5,2)),CaseVide((5,3)),CaseVide((5,4)),CaseVide((5,5)),CaseVide((5,6)), CaseVide((5,7))],
                            [CaseVide((6,i)) for i in range(8)],
                            [CaseVide((7,i))for i in range(8)]]

            self.cr_blanc = (7,4)
            self.cr_noir = (0,4)
        def __repr__(self):
            ch=""
            
            for i in range(len(self.echiquier)):
                ch += "\n | "
                for j in range(len(self.echiquier[i])):
                    if self.echiquier[i][j]!=0:
                        ch = ch + f"{self.echiquier[i][j].valeur}" + "| "
                    else:
                        ch += " 0 |"

            return ch



        def echec(self, couleur):
            """
            Fonction pour vérifier si échec
            Necessitera une copie de echec pour vérifier si le mouvement d'un pion entrainera un echec
            """
            if couleur == "noir": # Verification echec sur roi noir
                for i in range(len(self.echiquier)):
                    for j in range(len(self.echiquier[i])):
                        if self.echiquier[i][j].couleur == "blanc": #Optimiosation

                            if self.cr_noir in self.echiquier[i][j].coup_possible(self, False):
                                return True
            else:
                for i in range(len(self.echiquier)):
                    for j in range(len(self.echiquier[i])):
                        if self.echiquier[i][j].couleur == "noir": #Optimisation

                            if self.cr_blanc in self.echiquier[i][j].coup_possible(self, False):
                                return True
            return False

        def pat(self):
            """
            Fonction pour vérifier si pat

            On pacours tout si un des deux camps ne peux plus bougr alors c'est pat (On a vérifier avant si il n'y a pas echec)
            """
            blanc = []
            noir = []
            for i in range(len(self.echiquier)):
                for j in range(len(self.echiquier[i])):
                    if self.echiquier[i][j].couleur =="blanc" and self.echiquier[i][j].coup_possible(self, True) != []:
                        blanc.append(self.echiquier[i][j].coup_possible(self, True))
                    elif self.echiquier[i][j].couleur =="noir" and self.echiquier[i][j].coup_possible(self, True) != []:
                        noir.append(self.echiquier[i][j].coup_possible(self, True))
            if blanc == [] or noir == []:
                return True
            return False

        def echec_et_mat(self,pat, couleur):
            """
            Methode pour vérifier si un joueur est echec et mat :
                - pat + echec
            Entree :
                - pat : booléen, permet un gain de temps en vérifiant si il y a pat avant dans la boucle au lieu de le revérifier ici
                -couleur : str, couleur du joueur
            Sortie :
                -booléen, True si echec et mat
                """
            if pat == True and self.echec(couleur) == True:
                return True
            return False

    #FONCTIONNE AVEC BLANC / NOIR
    #Probleme quand on mange une pièce -> voir pour faire un bonus ou un truc comme ça
    E = Echiquier()
    print(E)
    pos = meilleur_coup(E, 3, "blanc")
    print(E)
    print(E.echiquier[pos[0][0]][pos[0][1]])
    E.echiquier[5][0].avancer((4,0), E)
    print(E.echiquier[pos[0][1]][pos[0][1]])
    print(E)
    pos = meilleur_coup(E, 3, "blanc")
    print(E)
    print(pos[0][1])
    E.echiquier[4][0].avancer((pos[0][1]), E)
    print(E)

    #pos=min_max(E.echiquier, "blanc", 1)
    #E.echiquier[pos[0][0][0]][pos[0][0][1]].avancer((pos[0][1][0], pos[0][1][1]), E.echiquier)

