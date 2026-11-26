# -*- coding: utf-8 -*-
"""
Fonction : 
    - joue_coup() : Meme principe que dans IA
    - annule_coup() : Meme principe que dans IA

Toutes les pièces :
    - Case vide 
    - Pion
    - Roi
    - Cavalier
    - Fou
    - Tour
    - Reine/Dame
"""
#Utiliser pour la vérification en cas d'échec
def joue_coup(jeu, entree, sortie):
    """ Joue un coup donnée
    entree : La coordonne de départ
    sortie : arrive
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


#Classe pour les différentes pièces 
class CaseVide:
    def __init__(self, position):
        self.valeur = 0
        self.position = position
        self.couleur = "Aucune"

    def avancer(self, _, __):
        return 
    
    def coup_possible(self, _, __ = True):
        return []

class Pion:
    """
    Pion :
        - couleur : "blanc" ou "noir"
        - position : tuple, (ligne, colonne)
        - debut : booléen pour savoir si pas de 2
        - valeur : 1 ou -1 
     Methode:
        - avancer : Avance le Pion + verifie si promotion en Dame
        - promotion : Modifie le pion en Dame
        - coup_possible : Renvoie un tableau avec tous les coups possibles
        - test_echec : Verifie si le coup est possible sans echec
    """
    
    def __init__(self, couleur, position, debut = True):
        self.couleur=couleur
        self.position = position
        self.debut = debut
        self.valeur=1 if couleur =="blanc" else -1


    def avancer(self, arrive,tab):
        """ Valeur : 1 / -1
        Avance le Pion + verifie si promotion en Dame
        Entree :
         - self
         - arrive : coordonée d'arrivée
         - tab : La classe Echiquier
        Sortie :
         -Rien le tableau est juste modifié"""

        if arrive in self.coup_possible(tab, True):
            self.position, pos = arrive, self.position #On déplace + on remet une caseVide -> pos garde l'ancienne position
            tab.echiquier[self.position[0]][self.position[1]], tab.echiquier[pos[0]][pos[1]] = self,CaseVide(self.position)
            self.debut=False
            
            self.promotion(tab)
        return self.position

    def promotion(self, tab):
        """
        Modifie le pion en Dame
        Entree :
            - tab : La classe Echiquier
            """
        #Verification pour promotion 
        echiquier= tab.echiquier
        if self.position[0] in [7, 0]:
                echiquier[self.position[0]][self.position[1]] = Dame(self.couleur, self.position)
              
    def coup_possible(self, tab, verifier_echec = True):
            """
            Renvoie un tableau avec tous les coups possibles
            Entrée : 
             - self : tout est dit
             - tab: La classe Echiquier
             
            Sortie : 
             - Un tableau répertoriant toute les possibilitées pour un pion
             
            Objectif :
             - Permettre la vérification dans la fonction avancée, et permettre une implemenation d'une IA"""
            possibilite = []
            coup_possiblepion = ((2,0), (1,1), (1,-1), (1,0)) #Le pion est en (0,0)
            for i in coup_possiblepion:
                arrive=self.position
                if self.couleur == 'noir': #On vérifie si l'arrivée est sur le plateau
                    arrive = (arrive[0] + i[0], arrive[1] + i[1])
                    if 0<=arrive[0] <= len(tab.echiquier)-1 and 0<=arrive[1]<=len(tab.echiquier[0])-1: #La position d'arrivée est dans l'echequier
                        if self.debut and arrive[0] == self.position[0] + 2 and self.position[1] == arrive[1] and tab.echiquier[arrive[0]][arrive[1]].valeur == 0 and tab.echiquier[arrive[0]-1][arrive[1]].valeur == 0: 
                            #Avance de deux cases 
                            #Verifie si on est bein au premier coup ET 2 cases de distances ET meme colonne ET case vide ET la case d'avant est vide 
                            possibilite.append(arrive)
                        elif arrive[1] != self.position[1] and abs(arrive[1]-self.position[1]) == 1 and tab.echiquier[arrive[0]][arrive[1]].valeur >0 : 
                            #Mange
                            #Verifie si la colonne est bien différente ET que la distance est 1 ET que la piece est bien une pièce ennemi
                            possibilite.append(arrive)
                        elif arrive[0] == self.position[0] + 1 and self.position[1] == arrive[1] and tab.echiquier[arrive[0]][arrive[1]].valeur == 0: 
                            #Avancer d'une case
                            #Verifie si c'est bien à une case de distance ET meme colonne ET que la case est vide
                            possibilite.append(arrive)

                else:
                    arrive = (arrive[0] - i[0], arrive[1] - i[1])
                    
                    if 0 <= arrive[0] <= len(tab.echiquier)-1 and 0<=arrive[1]<=len(tab.echiquier[0])-1:
                        if self.debut and arrive[0] == self.position[0] - 2 and self.position[1] == arrive[1] and tab.echiquier[arrive[0]][arrive[1]].valeur == 0 and tab.echiquier[arrive[0] + 1][arrive[1]].valeur == 0: 
                            #Avance de deux cases 
                            #Verifie si on est bein au premier coup ET 2 cases de distances ET meme colonne ET case vide ET la case d'avant est vide 
                            possibilite.append(arrive)
                        elif arrive[1] != self.position[1] and abs(arrive[1]-self.position[1]) == 1 and tab.echiquier[arrive[0]][arrive[1]].valeur < 0: 
                            #Mange
                            #Verifie si la colonne est bien différente ET que la distance est 1 ET que la piece est bien une pièce ennemi
                            
                            possibilite.append(arrive)
                        
                        elif arrive[0] == self.position[0] - 1 and self.position[1] == arrive[1] and tab.echiquier[arrive[0]][arrive[1]].valeur == 0:
                            #Avancer d'une case
                            #Verifie si c'est bien à une case de distance ET meme colonne ET que la case est vide
                            
                            possibilite.append(arrive)
                        
            if verifier_echec == True:

                return self.test_echec(tab, possibilite)
            else:
                return possibilite
    
    def test_echec(self, tab, possibilite):
        """
        Modifie le tableau des coups possibles en supprimant les coups illégaux
        Entree : 
            - tab : La classe Echiquier
            - possibilite : tableau des coups possibles
        Sortie :
            - new_possibilite : tableau des coups possibles sans les mises en échecs
        """
        new_possibilite = []
        for i in possibilite:
            entree = self.position
            mange, piece = joue_coup(tab, entree, i)
            if self.couleur == "noir" and tab.echec("noir") != True:
                new_possibilite.append(i)
            elif self.couleur == "blanc" and tab.echec("blanc") != True:
                new_possibilite.append(i)
            annule_coup(tab, entree, i, mange, piece)

        return new_possibilite
            
class Roi:
    """
    Roi :
        - couleur : La couleur de la pièce
        - position : tuple, (ligne, colonne)
        - roque : booleen pour savoir si roque possible (INACTIF)
        - valeur : 800 ou -800
     Methode :
        - echec : verifie si echec (INACTIF)
        - avancer : Avance le roi au coordonnée données
        - coup_possible : Donne tout les coups possible dans la position actuelle
        - test_echec : Verifie si le coup est possible sans echec
        """
    
    def __init__(self, couleur, position):
        self.couleur = couleur
        self.position = position 
        self.roque = False
        self.valeur = 800 if couleur =="blanc" else -800
        self.coup = []

    def avancer(self, arrive, tab):
        """ Valeur : 800 / -800
        Avance le roi au coordonnée données
        Entree :
         - self
         - arrive : coordonée d'arrivée
         - tab : La classe Echiquier
        Sortie :
         -Rien : le tableau est juste modifié"""
 

        if arrive in self.coup_possible(tab):
            pos, self.position = self.position, arrive #On déplace + on remet une caseVide
            tab.echiquier[pos[0]][pos[1]],tab.echiquier[self.position[0]][self.position[1]] =CaseVide(pos), self
            
            if self.couleur == "blanc":
                tab.cr_blanc = self.position 
            else:
                tab.cr_noir = self.position
                
    def coup_possible(self, tab, verifier_echec = True):
        """
        Donne tout les coups possible dans la position actuelle
        Entree :
         - tab : La classe Echiquier
         - verifier_echec : booleen (permet d'éviter une boucle infinie dans la fonction test_echec)
        Sortie : 
         - Un tableau avec toute les possibilitées comme pour le pion"""
        coup_possible_roi = ((0,1), (1, 0), (0,-1) , (1, -1), (1,1) , (-1, -1), (-1, 0), (-1, 1))
        possibilite = []

        for i in coup_possible_roi:
            arrive = self.position

            if self.couleur == "noir":
                arrive = (arrive[0] + i[0], arrive[1] + i[1])
                
                if 0<=arrive[0] <= len(tab.echiquier)-1 and 0<=arrive[1]<=len(tab.echiquier[1])-1: #Dans l'échiquier
                    
                    if arrive[1] != self.position[1] and abs(arrive[1]-self.position[1]) == 1 and tab.echiquier[arrive[0]][arrive[1]].valeur >= 0: #Se déplace sur les cotés
                        possibilite.append(arrive)
                    elif (arrive[0] == self.position[0] + 1 or arrive[0] == self.position[0] - 1) and tab.echiquier[arrive[0]][arrive[1]].valeur >= 0:
                        possibilite.append(arrive)

            else:
                arrive = (arrive[0] - i[0], arrive[1] - i[1])
                if 0<=arrive[0] <= len(tab.echiquier)-1 and 0<=arrive[1]<=len(tab.echiquier[1])-1: #Dans l'échiquier
                    if arrive[1] != self.position[1] and abs(arrive[1]-self.position[1]) == 1 and tab.echiquier[arrive[0]][arrive[1]].valeur <= 0: #Se déplace sur les cotés
                        possibilite.append(arrive)
                    elif (arrive[0] == self.position[0] + 1 or arrive[0] == self.position[0] - 1) and tab.echiquier[arrive[0]][arrive[1]].valeur <= 0:
                        possibilite.append(arrive)

        
        if verifier_echec == True:
                return self.test_echec(tab, possibilite)
        else:
                self.coup = possibilite
                return possibilite

    def test_echec(self, tab, possibilite): #Probleme avec le roi, prends des fois en compte et des fois pas
        """
        Renvoie un tableau sans les coups illégaux
        Entree :
         - tab : La classe Echiquier
         - possibilite : tableau des coups possibles
        Sortie : 
            - new_possibilite : tableau des coups possibles sans les mises en échecs
        """
        new_possibilite = []
        for i in possibilite:
            entree = self.position
            mange, piece = joue_coup(tab, entree, i)
            if self.couleur == "noir": #On modifie temporairement la valeur de cr_noir
                tab.cr_noir = i
                if tab.echec("noir") != True:
                    new_possibilite.append(i)
                tab.cr_noir = entree
            elif self.couleur == "blanc":
                tab.cr_blanc = i
                if tab.echec("blanc") != True:
                    new_possibilite.append(i)
                tab.cr_blanc = entree
            annule_coup(tab, entree, i, mange, piece)
        self.coup = new_possibilite
        return self.coup

class Cavalier:
    
    """
    Cavalier :
        - couleur : "blanc" ou "noir"
        - position : tuple, (ligne, colonne)
        - valeur : 3 ou -3 
     Methode:
        - avancer : Déplace le Cavalier
        - coup_possible : Renvoie un tableau avec tous les coups possibles
        - test_echec : Verifie si le coup est possible sans echec
    """
    def __init__(self, couleur, position):
        self.couleur = couleur
        self.position = position
        self.valeur = -2 if couleur =="noir" else 2
        self.coup = []

    def avancer(self, arrive, tab):
        """ Valeur : -3 / 3
        Déplace le Cavalier
        Entree :
         - self
         - arriver : coordonée d'arrivée
         - tab : La classe Echiquier
        Sortie :
         -Rien : le tableau est juste modifié (les coordonnées aussi)"""
        if arrive in self.coup_possible(tab):
            self.position, pos=arrive, self.position #On déplace + on remet une caseVide -> pos garde l'ancienne position
            tab.echiquier[self.position[0]][self.position[1]], tab.echiquier[pos[0]][pos[1]] =self,CaseVide(self.position)
        
    def coup_possible(self, tab, verifier_echec = True):
        """
        Renvoie un tableau avec tous les coups possibles
        Entrée :
         - tab : La classe Echiquier / Vérifier si on ne mange pas on propre pion
        Sortie : 
         - Un tableau avec toute les possibilitées comme pour le pion
         - verifier_echec : booleen (permet d'éviter une boucle infinie dans la fonction test_echec)
     """
        coup_possible = ((-2, 1), (-2, -1), (-1, -2), (1, -2), (2, 1), (2, -1), (1, 2),(-1, 2)) #Tous les L possibles
        possibilite = []

        for i in coup_possible:
            arrive = (self.position[0] + i[0], self.position[1] + i[1])
            if 0<=arrive[0] <= len(tab.echiquier)-1 and 0<=arrive[1]<=len(tab.echiquier[0])-1: #Dans l'echiquier
                if self.valeur > 0: #Blanc
                    if tab.echiquier[arrive[0]][arrive[1]].valeur <= 0:
                        possibilite.append(arrive)
                else:
                    if tab.echiquier[arrive[0]][arrive[1]].valeur >= 0:
                        possibilite.append(arrive)
        if verifier_echec == True:

                return self.test_echec(tab, possibilite)
        else:
                self.coup = possibilite
                return possibilite
    
    def test_echec(self, tab, possibilite):
        """
        Renvoie un tableau sans les coups illégaux
        Entree :    
         - tab : La classe Echiquier
         - possibilite : tableau des coups possibles
        Sortie :
         - new_possibilite : tableau des coups possibles sans les mises en échecs
         """
        new_possibilite = []
        for i in possibilite:
            entree = self.position
            mange, piece = joue_coup(tab, entree, i)
            if self.couleur == "noir" and tab.echec("noir") != True:
                new_possibilite.append(i)
            elif self.couleur == "blanc" and tab.echec("blanc") != True:
                new_possibilite.append(i)

            annule_coup(tab, entree, i, mange, piece)
        self.coup = new_possibilite
        return self.coup
    
class Tour:
    """
    Tour :
        - couleur : "blanc" ou "noir"
        - position : tuple, (ligne, colonne)
        - roque : booléen pour savoir si le roque est possible (INACTIF)
        - valeur : 5 ou -5 
     Methode:
        - avancer : Avance la Tour
        - coup_possible : Renvoie un tableau avec tous les coups possibles
        - test_echec : Verifie si le coup est possible sans echec
    """
    def __init__(self, couleur, position):
        self.couleur = couleur
        self.position = position
        self.valeur = 5 if couleur =="blanc" else -5
        self.roque = False
        self.coup = []
    
    def avancer(self, arrive, tab):
        """ Valeur : 5 / -5
        Avance la tour au coordonnée données
        Entree :
         - self
         - arrive : coordonée d'arrivée
         - tab : la classe Echiquier
        Sortie :
         -Rien : le tableau est juste modifié"""
 
        
        if arrive in self.coup_possible(tab):
            tab = tab.echiquier
            pos, self.position = self.position, arrive #On déplace + on remet une caseVide
            tab[pos[0]][pos[1]], tab[self.position[0]][self.position[1]] =CaseVide(pos), self
    
    def coup_possible(self, obj, verifier_echec = True):
        """
        Donne tout les coups possible dans la position actuelle
        Entree :
         - obj : La classe Echiquier
        Sortie : 
         - Un tableau avec toute les possibilitées
         - verifier_echec : booleen (permet d'éviter une boucle infinie dans la fonction test_echec)"""
        coup_possible= ((1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2), (3, 0),
                        (-3, 0), (0, 3), (0, -3), (4, 0), (-4, 0), (0, 4), (0, -4), (5, 0), (-5, 0), 
                        (0, 5), (0, -5), (6, 0), (-6, 0), (0, 6), (0, -6), (7, 0), (-7, 0), (0, 7), 
                        (0, -7) )
        possibilite = []
        tab = obj.echiquier
        for i in coup_possible:
                if self.couleur == "blanc":
                    arrive = (self.position[0] - i[0], self.position[1] - i[1])
                    if 0 <= arrive[0] <= len(tab)-1 and 0 <= arrive[1] <=len(tab[0])-1:
                       
                        if arrive[0] != self.position[0] and arrive[1] == self.position[1] and tab[arrive[0]][arrive[1]].valeur <= 0: 
                            
                            #pour déplacer la tour de haut en bas; on verifie si la ligne est differente et si la colonne est la meme (les 2 ne peuvent 
                            #pas etre différent en meme temps, sinon ca veut dire qu'on bouge en diagonale) 


                            #On ajoute la valeur à possibilité
                            if arrive[0] < self.position[0]: # Si la tour monte 
                                possibilite.append(arrive)
                                
                                #On parcours le tableau et si une case différente de 0 sur la trajectoire, on retire la possibilité
                                for i in range(arrive[0] + 1, self.position[0]):
                                    if tab[i][arrive[1]].valeur != 0:
                                        del possibilite[len(possibilite)-1]
                                        break

                            else: #Si la tour descend
                                possibilite.append(arrive)
                                for i in range(self.position[0] + 1, arrive[0]): #Verifie si les cases entre l'arrivée et la position sont vides
                                    

                                    if tab[i][arrive[1]].valeur != 0:
                                      del possibilite[len(possibilite)-1]
                                      break
                            

                            
                        
                        elif arrive[0] == self.position[0] and arrive[1] != self.position[1] and tab[arrive[0]][arrive[1]].valeur <= 0: 
                            #pour déplacer de gauche a droite; on suit le meme principe,la colonne et la ligne peuvent pas être differente en meme temps

                            possibilite.append(arrive)#On ajoute la valeur à possibilité
                            if arrive[1] < self.position[1]:
                                #On parcours le tableau et si une case différente de 0 sur la trajectoire, on retire
                                for i in range(arrive[1] + 1, self.position[1]):
                                    
                                    if tab[arrive[0]][i].valeur != 0:
                                        del possibilite[len(possibilite)-1]
                                        break
                            else:
                                
                                for i in range(self.position[1] + 1, arrive[1]):
                                    
                                    if tab[arrive[0]][i].valeur != 0:
                                        del possibilite[len(possibilite)-1]
                                        break
                        
                #Fonctionne NORMALEMENT...
                else: #Noir
                    arrive = (self.position[0] + i[0], self.position[1] + i[1])
                    if 0<=arrive[0] <= len(tab)-1 and 0<=arrive[1]<=len(tab[0])-1:
                        
                        #bouger tour de haut en bas
                        if arrive[0] != self.position[0] and arrive[1] == self.position[1] and tab[arrive[0]][arrive[1]].valeur >= 0: 
                            #On ajoute la valeur à possibilité
                            possibilite.append(arrive)
                        # MONTER
                            if arrive[0] < self.position[0]:
                                
                                #On parcours le tableau et si une case différente de 0 sur la trajectoire, on retire
                                for i in range(arrive[0] + 1, self.position[0] - 1):
                                    
                                    if tab[i][arrive[1]].valeur != 0:
                                        del possibilite[len(possibilite)-1]
                                        break
                        #DESCENTE
                            else: 
                                
                                for i in range(self.position[0]+1, arrive[0]):
                                    
                                    if tab[i][arrive[1]].valeur != 0 :
                                        del possibilite[len(possibilite)-1]
                                        break
                    #de gauche a droite
                        elif arrive[0] == self.position[0] and arrive[1] != self.position[1] and tab[arrive[0]][arrive[1]].valeur >= 0: 
                             
                            #On ajoute la valeur à possibilité
                            possibilite.append(arrive)
                        #COTE DROIT
                            if arrive[1] < self.position[1]:
                                #On parcours le tableau et si une case différente de 0 sur la trajectoire, on retire
                           
                                for i in range(arrive[1] + 1, self.position[1]): 

                                    if tab[arrive[0]][i].valeur != 0:
                                        del possibilite[len(possibilite)-1]
                                        break
                        #COTE GAUCHE 
                            else:
                                for i in range(self.position[1] + 1, arrive[1]):
                                    
                                    if tab[arrive[0]][i].valeur != 0:
                                        del possibilite[len(possibilite)-1]
                                        break
        if verifier_echec == True:

                return self.test_echec(obj,  possibilite)
        else:
                self.coup = possibilite
                return possibilite

    def test_echec(self, tab, possibilite):
        """
        Renvoie un tableau sans les coups illégaux
        Entree :
         - tab : La classe Echiquier
         - possibilite : tableau des coups possibles
        Sortie :
         - new_possibilite : tableau des coups possibles sans les mises en échecs
        """
        new_possibilite = []
        for i in possibilite:
            entree = self.position
            mange, piece = joue_coup(tab, entree, i)
            if self.couleur == "noir" and tab.echec("noir") != True:
                new_possibilite.append(i)
            elif self.couleur == "blanc" and tab.echec("blanc") != True:
                new_possibilite.append(i)

            annule_coup(tab, entree, i, mange, piece)
        self.coup = new_possibilite
        return self.coup

class Fou:
    """Fou :
        - couleur : "blanc" ou "noir"
        - position : tuple, (ligne, colonne)
        - valeur : 3 ou -3
     Methode:
        - avancer : Avance le Pion + verifie si promotion en Dame
        - coup_possible : Renvoie un tableau avec tous les coups possibles
        - test_echec : Verifie si le coup est possible sans les coups illégaux
    """
    def __init__(self, couleur, position):
        self.couleur = couleur
        self.position = position
        self.valeur = 3 if couleur =="blanc" else -3
        self.coup = []

    def avancer(self, arrive,tab):
         """ Valeur : 5 / -5
         Avance le fou au coordonnée données
         Entree :
          - self
          - arrive : coordonée d'arrivée
          - tab : le tableau d'affichage
         Sortie :
          -Rien : le tableau est juste modifié"""
  

         if arrive in self.coup_possible(tab):
             tab= tab.echiquier
             pos, self.position = self.position, arrive #On déplace + on remet une caseVide
             tab[pos[0]][pos[1]], tab[self.position[0]][self.position[1]] =CaseVide(pos), self

    def coup_possible(self,obj, verifier_echec = True):
        """
        Donne tout les coups possible dans la position actuelle
        Entree :
         - obj : La classe Echiquier
        Sortie : 
         - Un tableau avec toute les possibilitées
         - verifier_echec : booleen (permet d'éviter une boucle infinie dans la fonction test_echec)"""
        coup_possible= ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1), (-1, 1)
                        , (1, -1), (-2, -2), (-2, 2), (2, -2), (-3, -3), (-3, 3), (3, -3), (-4, -4), 
                        (-4, 4), (4, -4), (-5, -5), (-5, 5), (5, -5), (-6, -6), (-6, 6), (6, -6), 
                        (-7, -7), (-7, 7), (7, -7) )
        possibilite = []
        tab = obj.echiquier
        for i in coup_possible:
            if self.couleur == "blanc":
                   arrive = (self.position[0] - i[0], self.position[1] - i[1])
                   if 0 <= arrive[0] <= len(tab)-1 and 0 <= arrive[1] <=len(tab[0])-1:

                       if arrive[0] != self.position[0] and arrive[1] != self.position[1] and tab[arrive[0]][arrive[1]].valeur <= 0:
                          possibilite.append(arrive)
                          
                          #Verif pour éviter jump
                          x = self.position
                          if i[0] > 0 and i[1] > 0:
                              pas = (1, 1)
                          elif i[0] > 0 and i[1] < 0:
                              pas = (1,-1)
                          elif i[0] < 0 and i[1] > 0:
                              pas = (-1, 1)
                          else:
                              pas = (-1,-1)
                          
                          
                          x = (x[0] - pas[0], x[1] - pas[1])
                          #Bonne idée mais le pas marche pas
                          while arrive != x:
                              
                              if tab[x[0]][x[1]].valeur != 0:
                                  
                                  del possibilite[len(possibilite) - 1]
                                  break
                                  
                              else:
                                  x = (x[0] - pas[0], x[1] - pas[1])
            else: #Noir
                   arrive = (self.position[0] + i[0], self.position[1] + i[1])
                   if 0<=arrive[0] <= len(tab)-1 and 0<=arrive[1]<=len(tab[0])-1:
                       
                       
                       if arrive[0] != self.position[0] and arrive[1] != self.position[1] and tab[arrive[0]][arrive[1]].valeur >= 0: 
                           #On ajoute la valeur à possibilité
                           possibilite.append(arrive)
                           
                           #Verif pour éviter jump
                           x = self.position
                           if i[0] > 0 and i[1] > 0:
                               pas = (1, 1)
                           elif i[0] > 0 and i[1] < 0:
                               pas = (1,-1)
                           elif i[0] < 0 and i[1] > 0:
                               pas = (-1, 1)
                           else:
                               pas = (-1,-1)
                           
                           
                           x = (x[0] + pas[0], x[1] + pas[1])
                           #Bonne idée mais le pas marche pas
                           while arrive != x:
                               
                               
                               if tab[x[0]][x[1]].valeur != 0:
                                   
                                   del possibilite[len(possibilite) - 1]
                                   break
                                   
                               else:
                                   x = (x[0] + pas[0], x[1] + pas[1])
                          
        if verifier_echec == True:

                return self.test_echec(obj, possibilite)
        else:
                self.coup = possibilite
                return possibilite

    def test_echec(self, tab, possibilite):
        """
        Renvoie un tableau sans les coups illégaux
        Entree :
         - tab : La classe Echiquier
         - possibilite : tableau des coups possibles
        Sortie :
         - new_possibilite : tableau des coups possibles sans les mises en échecs
        """
        new_possibilite = []
        for i in possibilite:
            entree = self.position
            mange, piece = joue_coup(tab, entree, i)
            if self.couleur == "noir" and tab.echec("noir") != True:
                new_possibilite.append(i)
            elif self.couleur == "blanc" and tab.echec("blanc") != True:
                new_possibilite.append(i)

            annule_coup(tab, entree, i, mange, piece)
        self.coup = new_possibilite
        return self.coup

class Dame:
    """
    Dame : 
        - couleur : "blanc" ou "noir"
        - position : tuple, (ligne, colonne)
        - valeur : 9 ou -9
     Methode :
        - avancer : deplace la pièce
        - coup_possible : renvoie tous les coups possibles
    """
    def __init__(self, couleur, position):
        self.couleur = couleur
        self.position = position 
        self.valeur = 9 if couleur =="blanc" else -9
        self.coup = []
        
    def avancer(self, arrive,tab):
        """ Valeur : 5 / -5
        Avance la dame au coordonnée données
        Entree :
         - self
         - arrive : coordonée d'arrivée
         - tab : la classe Echiquier
        Sortie :
         -Rien : le tableau est juste modifié"""
 

        if arrive in self.coup_possible(tab):
            tab=tab.echiquier
            pos, self.position = self.position, arrive #On déplace + on remet une caseVide
            tab[pos[0]][pos[1]],tab[self.position[0]][self.position[1]] =CaseVide(pos), self

    def coup_possible(self, obj, verifier_echec = True):
        coup_possible = ((1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2), (3, 0),
                        (-3, 0), (0, 3), (0, -3), (4, 0), (-4, 0), (0, 4), (0, -4), (5, 0), (-5, 0), 
                        (0, 5), (0, -5), (6, 0), (-6, 0), (0, 6), (0, -6), (7, 0), (-7, 0), (0, 7), 
                        (0, -7), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (-1, -1),
                        (-1, 1), (1, -1), (-2, -2), (-2, 2), (2, -2), (-3, -3), (-3, 3), (3, -3), 
                        (-4, -4), (-4, 4), (4, -4), (-5, -5), (-5, 5), (5, -5), (-6, -6), (-6, 6), (6, -6), 
                        (-7, -7), (-7, 7), (7, -7))
        possibilite = []
        tab = obj.echiquier
        for i in coup_possible:
            
                if self.couleur == "blanc": #Ca fait peur mais ça va
                    arrive = (self.position[0] - i[0], self.position[1] - i[1])
                    if 0<=arrive[0] <= len(tab)-1 and 0<=arrive[1]<=len(tab[0])-1:
                        if arrive in Tour(self.couleur, self.position).coup_possible(obj, False) or arrive in Fou(self.couleur, self.position).coup_possible(obj, False):
                            possibilite.append(arrive)
                else: #Ca fait peur mais ça va
                    arrive = (self.position[0] + i[0], self.position[1] + i[1])
                    if 0<=arrive[0] <= len(tab)-1 and 0<=arrive[1]<=len(tab[0])-1:
                        if arrive in Tour(self.couleur, self.position).coup_possible(obj, False) or arrive in Fou(self.couleur, self.position).coup_possible(obj, False):
                            possibilite.append(arrive)
        if verifier_echec == True:

                return self.test_echec(obj, possibilite)
        else:
                self.coup = possibilite
                return possibilite                
        
    
    def test_echec(self, tab, possibilite):
        new_possibilite = []
        for i in possibilite:
            entree = self.position
            mange, piece = joue_coup(tab, entree, i)
            if self.couleur == "noir" and tab.echec("noir") != True:
                new_possibilite.append(i)
            elif self.couleur == "blanc" and tab.echec("blanc") != True:
                new_possibilite.append(i)

            annule_coup(tab, entree, i, mange, piece)
        self.coup = new_possibilite
        return self.coup
