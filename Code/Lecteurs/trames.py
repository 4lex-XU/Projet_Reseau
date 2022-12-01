import numpy as np
def diviseurDeTrame(fichier) :
    """
    Entrée : un fichier texte, contenant une ou plusieurs trames
    Sortie : un tableau de trame
    Dans le fichier texte, chaque trame termine par un unique saut de ligne '\n'
    """
    
    fichier = open(fichier, "r")
    # tableau de ligne 
    lignes = fichier.readlines()
    fichier.close()
    
    i = 0
    new_trame = False
    trames = []
    trame = ""
    
    for ligne in lignes :
        # on regarde si c'est le début d'une nouvelle trame, sauf pour la première
        if(ligne[0:7] == "0000   " and i != 0) :
            new_trame = True
        # si c'est le début d'une nouvelle trame, on ajoute la trame précédente au tableau
        if(new_trame) :
            # on ajoute la trame sans les espaces
            trames.append(trame.replace(" ",""))
            trame = ""
            new_trame = False
        # on ajoute la ligne à la trame sans offset
        trame += ligne[7:-1]
        # on enlève la condition de la 1ère trame
        i+=1
        
    # on ajoute la dernière trame au tableau
    trames.append(trame.replace(" ",""))
    
    return trames

