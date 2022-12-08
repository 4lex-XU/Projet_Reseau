import sys
sys.path.append("..")
from Convertisseurs.hexaToBinary import *

def lectureTCP(trame):
    if(trame is None):
        print("Trame vide")
        return None
    HTTP = -1
    PortSrc = trame[0:4]
    #REPLY = 1
    if(PortSrc == "0050"):
        HTTP = 1
    PortDest = trame[4:8]
    #REQUEST = 0
    if(PortDest == "0050"):
        HTTP = 0
    #SI HTTP = -1 ALORS PAS DE CONNEXION A UN SERVEUR WEB (HTTP)
    THL = int(trame[24],16)
    Etat = hexaToBinary(trame[25:28])
    URG = Etat[6]
    ACK = Etat[7]
    PSH = Etat[8]
    RST = Etat[9]
    SYN = Etat[10]
    FIN = Etat[11]
    FLAGS = (URG,ACK,PSH,RST,SYN,FIN)
    Win = int(trame[28:32],16)
    #initialisation des variables pour le traitement des options
    MSS, SACK, TSval, TSecr, WS = (0,0,0,0,0)
    OPT = (MSS, SACK, TSval, TSecr, WS)
    if(THL > 5):
        #Option(s) TCP presente
        fin_entete = THL*8
        data = trame[fin_entete:]
        #TRAITEMENT DES OPTIONS
        option = trame[40:fin_entete]
        b = 0
        while(b < fin_entete):
            if(option[b:b+4] == "0204"):
                #Maximum Segment Size
                length = int(option[b+2:b+4],16)*2
                MSS = int(option[b+4:b+length],16)
                b += length
            if(option[b:b+4] == "0402"):
                #SACK Permitted
                SACK = 1
                length = int(option[b+2:b+4],16)*2
                b += length
            if(option[b:b+4] == "080a"):
                #Timestamps
                length = int(option[b+2:b+4],16)*2
                Timestamps = option[b+4:b+length]
                TSval = int(Timestamps[0:8],16)
                TSecr = int(Timestamps[8:],16)
                b += length
            if(option[b:b+4] == "0303"):
                #WindowScale
                length = int(option[b+2:b+4],16)*2
                WS = pow(2,int(option[b+4:b+length],16))
                b += length
            b += 2
        OPT = (MSS, SACK, TSval, TSecr, WS)
    else:
        data = trame[40:]
    return (HTTP, PortSrc, PortDest, THL, FLAGS, Win, OPT, data)

def checksumTCP(IPsrc, IPdest, Protocol, THL, portSrc, portDest, trame):
    if trame is None:
        print("Trame vide")
        return None
    somme = 0 
    somme += int(IPsrc[0:2],16)
    somme += int(IPsrc[2:4],16)
    somme += int(IPdest[0:2],16)
    somme += int(IPdest[2:4],16)
    somme += int(Protocol,16)
    somme += THL
    somme += int(portSrc,16)
    somme += int(portDest,16)

    i = 24
    while(i < len(trame)):
        somme += int(trame[i:i+2],16)
        i += 2
    
    binaire = bin(somme)[2:].zfill(16)    
    
    #print(binaire)
    taille = len(binaire)
    if(taille > 16):
        indice = taille - 16
        b = binaire[0:indice]
        binaire = binaire[indice:]
        somme = int(binaire,2)
        somme += int(b,2)
        binaire = hexaToBinary(hex(somme)[2:])
    
    return  binaire ==  "1111111111111111"

    