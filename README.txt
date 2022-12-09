ALEX XU - STEPHANIE HUANG

========================================================================================================

REPERTOIRES :
    Le projet est constitué de 3 dossiers :
        - Code : contient le code source du projet 
            - Convertisseur : les fonctions de conversions
            - Interface : la fonction pour construire l'interface graphique, et ses outils de filtrage
            - Lecteurs : les différentes fonctions pour décoder les trames, sous différentes couches
            - Tests : le main(), et un fichier test qu'on a utilisé pour tester nos fonctions
        - Traces : contient les fichiers de sauvegardes
        - Trames : contient les fichiers de trames pour les tests
    Nous avons laissé nos exemples de fichiers de trames pour les tests

=========================================================================================================

FONCTIONS MAJEURS: 
    - main() : 
        - prend en entrée un fichier texte, affiche un visualisateur de trame, et sauvegarde le visualisateur dans un fichier .txt 
        - la fonction utilise tous les lecteurs de trames, un diviseur de trame, ainsi que l'interface graphique
    - interface () : 
        crée un interface graphique sur Tkinter, il y a une fonction interne action() qui permet les actions de filtrage