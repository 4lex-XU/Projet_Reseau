import sys
sys.path.append("..")
from Convertisseurs.hexaToASCII import *

def lectureHTTPreq(trame) :
    if(trame is None):
        print("Trame vide")
        return None
    # determine la méthode de la requête
    indiceMeth = trame.find("20")
    methode = trame[0:indiceMeth]
    # on cherche le saut de ligne pour trouver l'adresse et la version
    indiceAddVer = trame.find("0d0a")
    # addresse et version
    contenu = trame[indiceMeth+2:indiceAddVer]
    
    # transforme le code hexa en ascii
    methode = hexaToASCII(methode)
    contenu = hexaToASCII(contenu)
    if(methode == None or contenu == None):
        return None

    return (methode, contenu)
    
def lectureHTTPrep(trame) :
    if(trame is None):
        print("Trame vide")
        return None
    # détermine la version 
    indiceVer = trame.find("20") # espace
    # détermine le code de réponse
    indiceCode = trame.find("20", indiceVer+2) # espace
    # détermine le message de réponse
    indiceMsg = trame.find("0d0a") # saut de ligne
    # détermine le type de contenu 
    indiceContentType1 = trame.find("436f6e74656e742d547970653a20") # Content-Type:
    indiceContentType2 = trame.find("0d0a", indiceContentType1) # saut de ligne
    
    # transforme le code hexa en ascii
    version = hexaToASCII(trame[0:indiceVer])
    code = hexaToASCII(trame[indiceVer+2:indiceCode])
    message = hexaToASCII(trame[indiceCode+2:indiceMsg])
    contentType = hexaToASCII(trame[indiceContentType1+28:indiceContentType2])
    if(version == None or code == None or message == None or contentType == None):
        return None

    return (version, code, message, contentType)