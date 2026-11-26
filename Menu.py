# -*- coding: utf-8 -*-

from Ressources import chemin_ressource
import pygame, sys
import Graphics
from Echiquier import Echiquier
pygame.init()

largeur = 60 * 8
hauteur = 60 * 8 #LE plus 10 pour afficher le tour 
class Game:
    def __init__(self):
        self.menu = False
        self.is_playing = False
        self.is_playing_IA = False
        self.is_playing_JvJ = False

class Button:

    def __init__(self, text, width, height, pos, action , elevation):
        self.pressed=False
        self.action=action
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        #Rectangle (position donner en haut à gauche)
        self.top_rect= pygame.Rect(pos, (width,height))
        self.top_color = "#475F77"

        #Estetic pour le rectangle
        self.bottom_rect = pygame.Rect(pos, (width, elevation))
        self.bottom_color = "#354B5E"

        #Text
        self.text_surf = gui_font.render(text, True, "#FFFFFF")
        self.text_rect = self.text_surf.get_rect(center = self.top_rect.center) #Prend la position du texte et place au milieu

    def draw(self): #Affiche le button et verifie si il n'y a pas de clcik
        #elevation logic / Estetique
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center= self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        #Affiche le boutton
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos): #Verifie si il y a une colision avec le bouton
            self.top_color='#D74B4B' #Estetique
            if pygame.mouse.get_pressed()[0]: #Le bouton gauche de la souris
                self.pressed=True
                #Estetique
                self.dynamic_elevation = 0

            else:
                self.dynamic_elevation = self.elevation

                if self.pressed==True: # Si l'on appuie pas, on remet à Faux et donc l'action s'active
                    if self.action == "Quit":
                        pygame.quit() #Effectue l'action
                        sys.exit()
                    elif self.action == "Jeu":
                        game.menu = True
                        
                    elif self.action == "JvJ":
                        game.menu = False
                        game.is_playing = True
                        game.is_playing_JvJ=True
                        Graphics.JvJ()
                    elif self.action == "Solo":
                        game.menu = False
                        game.is_playing = True
                        game.is_playing_IA=True
                        Graphics.play_IA()

                    self.pressed=False
        else:
            #Estetique
            self.dynamic_elevation = self.elevation
            self.top_color = "#475F77"

# Met en place l'écran + nom + temps
screen = pygame.display.set_mode((largeur,hauteur))
pygame.display.set_caption("Jeu d'Echec")
clock = pygame.time.Clock()
gui_font= pygame.font.Font(None, 30)



#Appelle les 4 boutons
StartGame=Button("JOUER", 200, 40, (largeur// 3 ,hauteur // 2), "Jeu", 6)
QuitGameButton=Button("Quitter", 200, 40, (largeur // 3 , hauteur // 2 + 50), "Quit",6)
SoloButton = Button("SOLO",200,40,(largeur// 3 ,hauteur // 2),"Solo", 6)
JvJButton = Button("Joueur VS Joueur", 200,40,(largeur//3, hauteur // 2 + 50), "JvJ", 6)
#Variable pour le jeu
game = Game()

#Les menus 
while True: 
    for event in pygame.event.get():        # Pour quitter le jeu avec la croix
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill("#84789A")
    if game.is_playing == False: 
        #Ajoute le titre 
        pygame.draw.rect(screen, "#84789A",pygame.Rect((largeur//3,0), (200,40)), )
        #screen.blit(gui_font.render("CHESS", True, "#c4bad9"), (largeur//3, 0))
        screen.blit(pygame.image.load(chemin_ressource("Image/Titre.png")), (largeur // 3 - 25, 0 ))
        
        if game.menu == True:
            JvJButton.draw()
            SoloButton.draw()
            
        else:
            #Appelle recurent pour verifier que le bouton n'a pas d'interraction
            StartGame.draw()
            QuitGameButton.draw()
    
    #Mets a jour le fond
    pygame.display.update()
    clock.tick(60)

        
