def lectureHTTPreq(trame) :
    # determine la méthode de la requête
    indiceMeth = trame.find("20")
    methode = trame[0:indiceMeth]
    # on cherche le saut de ligne pour trouver l'adresse et la version
    indiceAddVer = trame.find("0d0a")
    # addresse et version
    contenu = trame[indiceMeth+2:indiceAddVer]
    
    # transforme le code hexa en ascii
    methode = bytes.fromhex(methode).decode('ascii')
    contenu = bytes.fromhex(contenu).decode('ascii')
    
    return (methode, contenu)
    
def lectureHTTPrep(trame) :
    # détermine la version 
    indiceVer = trame.find("20")
    # détermine le code de réponse
    indiceCode = trame.find("20", indiceVer+2)
    # détermine le message de réponse
    indiceMsg = trame.find("0d0a")
    
    # transforme le code hexa en ascii
    version = bytes.fromhex(trame[0:indiceVer]).decode('ascii')
    code = bytes.fromhex(trame[indiceVer+2:indiceCode]).decode('ascii')
    message = bytes.fromhex(trame[indiceCode+2:indiceMsg]).decode('ascii')
    
    return (version, code, message)
    
