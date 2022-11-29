import numpy as np
def lecteurDeTrame(fichier) :
    
    fichier = open(fichier, "r")
    # tableau de ligne 
    lignes = fichier.readlines()
    fichier.close()
    
    i = 0
    new_trame = False
    trames = []
    trame = ""
    
    for ligne in lignes :
        if(ligne[0:7] == "0000   " and i != 0) :
            new_trame = True
        if(new_trame) :
            trames.append(trame)
            trame = ""
            new_trame = False
        trame += ligne[7:]
        i+=1
        
    trames.append(trame)
    
    return trames    
            
    #srcMac, dstMac, type = lectureEthernet(trame)
    #protocol, srcIP, dstIP = lectureIPv4(trame)
    #int(srcIP[0:2], 16)
  
def IPv4_dec(ip) :
    return str(int(ip[0:2], 16))\
        +"."+str(int(ip[2:4], 16))\
        +"."+str(int(ip[4:6], 16))\
        +"."+str(int(ip[6:8], 16))

def port_dec(port) :
    return str(int(port,16))

#tests
#print(IPv4_dec("3cb95740"))
print(lecteurDeTrame("tcp.txt"))