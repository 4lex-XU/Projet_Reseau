import sys
sys.path.append("..")
from Convertisseurs.hexaToBinary import *

def lectureIPv4(trame):
    #Trame vide
    if(trame is None):
        print("Trame vide")
        return None
    if(trame[28] != "4"):
        print("La version de IP ne correspond pas a IPv4")
        return None
    IHL = int(trame[29],16) # 5 = 20 octets
    option = False
    if(IHL > 5):
        #Option(s) IP presente
        option = True
    TotalLength = int(trame[32:36],16) - IHL*4 #Taille de la trame - taille de l'entete IP
    #TRAITEMENT DES FRAGMENTS
    fragment = hexaToBinary(trame[40:44])
    DF = fragment[1]
    MF = fragment[2]
    offset = int(fragment[3:],2)
    #print(offset)
    TTL = int(trame[44:46],16)
    protocol = trame[46:48] # 06 = TCP, 11 = UDP
    IPSrc = trame[52:60]
    IPDest = trame[60:68]
    return (IHL, protocol, IPSrc, IPDest, option, TotalLength, DF, MF, offset, TTL)
