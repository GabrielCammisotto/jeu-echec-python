# -*- coding: utf-8 -*-
"""
Jeu Echec/Echiquier

La partie fonctionnelle de l'echiquier
"""
from Piece import Dame, CaseVide, Pion, Roi, Tour, Cavalier, Fou
from IA import *

class Echiquier:
    """
    Echiquier :
        - echiquier : matrice représentant le plateau, les pièces sont représentées par leur object
        -__repr__ : renvoie l'echiquier dans l'IDE
        
    """
    def __init__(self):
        self.echiquier = [[Tour("noir", (0,0)), Cavalier("noir", (0,1)), Fou("noir", (0,2)), Dame("noir",(0,3)), Roi("noir", (0,4)), Fou("noir", (0,5)), Cavalier("noir", (0,6)), Tour("noir",(0,7))],
                          [Pion("noir", (1,i)) for i in range(8)],
                          [CaseVide((2,i))for i in range(8)],
                          [CaseVide((3,i))for i in range(8)],
                          [CaseVide((4,i))for i in range(8)],
                          [CaseVide((5,i))for i in range(8)],
                          [Pion("blanc", (6,i)) for i in range(8)],
                          [Tour("blanc", (7,0)), Cavalier("blanc", (7,1)), Fou("blanc", (7,2)), Dame("blanc",(7,3)), Roi("blanc", (7,4)), Fou("blanc", (7,5)), Cavalier("blanc", (7,6)), Tour("blanc",(7,7))]]
        self.cr_blanc = (7,4)
        self.cr_noir = (0,4)
    def __repr__(self):
       ch=""
       print(ch)
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
        nbpiece = 0#les autres raison qui amène un pat (que les deux rois / j'ai pas fait le vcavalier + fou)
        for i in range(len(self.echiquier)):
            for j in range(len(self.echiquier[i])):
                if self.echiquier[i][j].couleur =="blanc" and self.echiquier[i][j].coup_possible(self, True) != []:
                    blanc.append(self.echiquier[i][j].coup_possible(self, True))
                    nbpiece += 1
                elif self.echiquier[i][j].couleur =="noir" and self.echiquier[i][j].coup_possible(self, True) != []:
                    noir.append(self.echiquier[i][j].coup_possible(self, True))
                    nbpiece += 1
        if blanc == [] or noir == [] or nbpiece == 2:
            return True
        return False

    def echec_et_mat(self,pat, couleur):
        """
        Le joueur est en echec et mat, l'adversaire a gagné
        
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
    

if "__main__" == __name__:
    E= Echiquier()
    print(E)

    for i in range(30):
        coordonne = input("Quels pion voulez vous déplacer ? ")
        if coordonne =="X":
            break
        coordonne = coordonne.split(',')
        coordonne = [int(i) for i in coordonne]
        
        print("Voici les coups jouables :", E.echiquier[coordonne[0]][coordonne[1]].coup_possible(E))
        entree=input("Coup :")
        if entree =="X":
            break
        entree = entree.split(',')
        entree = (int(entree[0]), int(entree[1]))
        #print(entree)
        E.echiquier[coordonne[0]][coordonne[1]].avancer(entree,E)
        print(E)
        print(E.echec("noir"))
        """ 
        pos=min_max(E, "noir", 2)
        print(pos)
        E.echiquier[pos[0][0][0]][pos[0][0][1]].avancer(pos[0][1],E)
        print(E) """


