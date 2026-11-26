import sys
import os

def chemin_ressource(chemin_relatif):
    # Dans un .exe PyInstaller, les fichiers sont décompressés dans un dossier temporaire
    # dont le chemin est stocké dans sys._MEIPASS
    if hasattr(sys, "_MEIPASS"):
        base = sys._MEIPASS
    else:
        # Lancement normal avec Python : on part du dossier de ce fichier
        base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, chemin_relatif)