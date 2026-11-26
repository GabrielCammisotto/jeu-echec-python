from Ressources import chemin_ressource
import pygame, sys, random
from Echiquier import Echiquier

import IA


def JvJ():

    pygame.init()

    #rejouezButton = Button("Rejouer", 200, 50, (largeur//2 - 100, hauteur//2 + 100), "JvJ", 0)
    #menuButton = Button("Menu", 200, 50, (largeur//2 - 100, hauteur//2 + 200), "Menu", 0)

    taille_case = 60  # Taille d'une case de l'échiquier
    largeur, hauteur = taille_case * 8, taille_case * 8

    # Couleurs
    ROUGE = (255, 60, 60)
    BLEU = (100,100,255)
    JAUNE = (255,255,130)

    # Chargement des images
    echiquier_img = pygame.transform.scale(pygame.image.load(chemin_ressource("Image/Chess_BG_Full.png")), (largeur, hauteur))

    def charger_image_piece(piece):
        if piece.valeur != 0:  # Si ce n'est pas une case vide
            return pygame.transform.scale(pygame.image.load(chemin_ressource(f"Image/Piece/Chess_{piece.couleur}_{type(piece).__name__}.png")), (taille_case, taille_case))
        return None

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption("Partie en cours - c'est au tour des blancs")

    police = pygame.font.Font(None, 36)

    echiquier = Echiquier()

    piece_selectionnee = None  # Stocke la pièce sélectionnée
    coups_possibles = []  # Stocke les coups possibles de la pièce sélectionnée

    # Boucle principale
    joueur = "blanc" #LEs blancs commencent
    next_joueur = "noir"

    fin_de_partie = False, None
    while True:
        for event in pygame.event.get():   #prend tout les evenement que le joueur fait(clic de souris,ect)
            if event.type == pygame.QUIT: #si on quitte la fenetre
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:#si on clique
                colonne, ligne = event.pos[0] // taille_case, event.pos[1] // taille_case          #vérifie ou le joueur a cliquer
                piece = echiquier.echiquier[ligne][colonne]

                if piece_selectionnee is None:        #si on a pas deja cliquer sur une pièce on prend en memoire la piece cliquer
                    # Sélection d'une pièce
                    if piece.valeur != 0 and piece.couleur == joueur:
                        piece_selectionnee = piece
                        coups_possibles = piece.coup_possible(echiquier)
                else:
                    # Déplacement de la pièce
                    if (ligne, colonne) in coups_possibles and joueur == piece_selectionnee.couleur: # sinon on regarde les coups possibles de la pièce et on l'y deplace + verifie couleur du joueur
                        joueur, next_joueur = next_joueur, joueur
                        piece_selectionnee.avancer((ligne, colonne), echiquier)
                        #On verifie l'echec que en cas de déplacement
                        pat = echiquier.pat() #Gain en optimisation de 3/4 seconde Chercher un moyen d'optimisation si jamais
                        if echiquier.echec_et_mat(pat, "blanc"):
                            fin_de_partie = True, "noir"
                        elif echiquier.echec_et_mat(pat, "noir"):
                            fin_de_partie = True, "blanc"
                        elif pat:
                            fin_de_partie = True, "pat"
                    piece_selectionnee = None
                    coups_possibles = []

        # affichage de l'échiquier
        fenetre.blit(echiquier_img, (0, 0))

        # liserair bleu des possibles
        for coup in coups_possibles:
            pygame.draw.rect(fenetre, JAUNE, (coup[1] * taille_case, coup[0] * taille_case, taille_case, taille_case), 10)

        # affichage des pièces
        for i in range(8):
            for j in range(8):
                piece = echiquier.echiquier[i][j]
                image = charger_image_piece(piece)
                if image:
                    fenetre.blit(image, (j * taille_case, i * taille_case))


        pygame.display.set_caption(f"Partie en cours - c'est au tour des : {joueur}")
        if fin_de_partie == (True, "blanc"):
            fenetre.blit(police.render("Les blancs ont gagné", True, (255,255,255)), (largeur // 2 - 150, hauteur // 2 - 50))
            #rejouezButton.draw(fenetre)
            #menuButton.draw(fenetre)
        elif fin_de_partie == (True, "noir"):
            fenetre.blit(police.render("Les noirs ont gagné", True, (255,255,255)), (largeur // 2 - 150, hauteur // 2 - 50))
            #rejouezButton.draw(fenetre)
            #menuButton.draw(fenetre)
        elif fin_de_partie == (True, "pat"):
            fenetre.blit(police.render("Pat", True, (255,255,255)), (largeur // 2 - 150, hauteur // 2 - 50))
            #rejouezButton.draw(fenetre)
            #menuButton.draw(fenetre)
        pygame.display.flip()


def play_IA():
    pygame.init()

    taille_case = 60  # Taille d'une case de l'échiquier
    largeur, hauteur = taille_case * 8, taille_case * 8

    # Couleurs
    ROUGE = (255, 60, 60)
    BLEU = (100,100,255)
    JAUNE = (255,255,130)

    # Chargement des images
    echiquier_img = pygame.transform.scale(pygame.image.load(chemin_ressource("Image/Chess_BG_Full.png")), (largeur, hauteur))

    def charger_image_piece(piece):
        if piece.valeur != 0:  # Si ce n'est pas une case vide
            return pygame.transform.scale(pygame.image.load(chemin_ressource(f"Image/Piece/Chess_{piece.couleur}_{type(piece).__name__}.png")), (taille_case, taille_case))
        return None

    # Création de la fenêtre
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption(f"Partie en cours - l'écran noir siginfie que l'IA réfléchit")
    police = pygame.font.Font(None, 36)

    echiquier = Echiquier()

    piece_selectionnee = None  # Stocke la pièce sélectionnée
    coups_possibles = []  # Stocke les coups possibles de la pièce sélectionnée

    # Boucle principale
    couleuractuelle = "blanc"
    if random.randint(0,1) == 0: #On choisit aléatoirement le joueur qui commence
        joueurcouleur, IAcouleur = "noir", "blanc" #Premier joueur
    else:
        joueurcouleur, IAcouleur = "blanc", "noir"

    coup_jouer = False
    fin_de_partie = False, None

    while True:
        for event in pygame.event.get():   #prend tout les evenement que le joueur fait(clic de souris,ect)
            if event.type == pygame.QUIT: #si on quitte la fenetre
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:#si on clique
                colonne, ligne = event.pos[0] // taille_case, event.pos[1] // taille_case          #vérifie ou le joueur a cliquer
                piece = echiquier.echiquier[ligne][colonne]

                if piece_selectionnee is None:        #si on a pas deja cliquer sur une pièce on prend en memoire la piece cliquer
                    # Sélection d'une pièce
                    if piece.valeur != 0 and piece.couleur == couleuractuelle:
                        piece_selectionnee = piece
                        coups_possibles = piece.coup_possible(echiquier)
                else:
                    # Déplacement de la pièce
                    if (ligne, colonne) in coups_possibles and couleuractuelle == piece_selectionnee.couleur: # sinon on regarde les coups possibles de la pièce et on l'y deplace + verifie couleur du joueur
                        coup_jouer = True #On affiche le coup -> evite bug visuel
                        piece_selectionnee.avancer((ligne, colonne), echiquier)
                        couleuractuelle = IAcouleur #Changement de joueur
                    #On verifie l'echec que en cas de déplacement
                        pat = echiquier.pat() #Gain en optimisation de 3/4 seconde Chercher un moyen d'optimisation si jamais
                        if echiquier.echec_et_mat(pat, "blanc"):
                            fin_de_partie = True, "noir"
                        elif echiquier.echec_et_mat(pat, "noir"):
                            fin_de_partie = True, "blanc"
                        elif pat:
                            fin_de_partie = True, "pat"
                    piece_selectionnee = None
                    coups_possibles = []

        #Changmene tvignette en haut
        if couleuractuelle == IAcouleur:
            pygame.display.set_caption(f"Partie en cours - votre adversaire réfléchit")
        else:
            pygame.display.set_caption(f"Partie en cours - c'est votre tour")
        #Coup de l'IA
        #joue si coup_jouer == False and la couleur actuelle correspond et la partie n'est pas finie
        if coup_jouer == False and couleuractuelle == IAcouleur and fin_de_partie == (False, None):
            pos = IA.meilleur_coups(echiquier, 2, IAcouleur)

            echiquier.echiquier[pos[0][0]][pos[0][1]].avancer(pos[1],echiquier)
            couleuractuelle = joueurcouleur

            pat = echiquier.pat() #Gain en optimisation de 3/4 seconde Chercher un moyen d'optimisation si jamais
            if echiquier.echec_et_mat(pat, "blanc"):
                fin_de_partie = True, "noir"
            elif echiquier.echec_et_mat(pat, "noir"):
                fin_de_partie = True, "blanc"
            elif pat:
                fin_de_partie = True, "pat"

        if coup_jouer == True: # Le coup a été joué
            coup_jouer = False


        # affichage de l'échiquier
        fenetre.blit(echiquier_img, (0, 0))


        # liserair bleu des possibles
        for coup in coups_possibles:
            pygame.draw.rect(fenetre, JAUNE, (coup[1] * taille_case, coup[0] * taille_case, taille_case, taille_case), 10)

        # affichage des pièces
        for i in range(8):
            for j in range(8):
                piece = echiquier.echiquier[i][j]
                image = charger_image_piece(piece)
                if image:
                    fenetre.blit(image, (j * taille_case, i * taille_case))


        #Fin de partie
        if fin_de_partie == (True, "blanc"):
            fenetre.blit(police.render("Les blancs ont gagné", True, (255,255,255)), (largeur // 2 - 150, hauteur // 2 - 50))
        elif fin_de_partie == (True, "noir"):
            fenetre.blit(police.render("Les noirs ont gagné", True, (255,255,255)), (largeur // 2 - 150, hauteur // 2 - 50))
        elif fin_de_partie == (True, "pat"):
            fenetre.blit(police.render("Pat", True, (255,255,255)), (largeur // 2 - 150, hauteur // 2 - 50))


        pygame.display.flip()


