import sys
import subprocess

# Obtention du chemin vers l'interpréteur Python en cours d'exécution
python_path = sys.executable

# Liste des bibliothèques à installer
libraries = ['numpy', 'pandas', 'pandasgui', 'matplotlib']

# Fonction pour installer les bibliothèques via pip
def install_libraries(libs):
    for lib in libs:
        print(f"Installation de {lib}...")
        try:
            subprocess.check_call([python_path, '-m', 'pip', 'install', lib])
            print(f"{lib} installée avec succès !")
        except subprocess.CalledProcessError:
            print(f"Erreur lors de l'installation de {lib}.")

# Installation des bibliothèques
install_libraries(libraries)
