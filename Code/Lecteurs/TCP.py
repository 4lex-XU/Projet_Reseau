
def lectureTCP(trame):
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
    THL = trame[24]
    Etat = trame[25:28]
    #CONVERSION BINAIRE
    binaire = ""
    for i in Etat:
        hexa_to_dec = int(i,16)
        binaire += bin(hexa_to_dec)[2:].zfill(4)
    #print(binaire)
    URG = binaire[6]
    ACK = binaire[7]
    PSH = binaire[8]
    RST = binaire[9]
    SYN = binaire[10]
    FIN = binaire[11]
    FLAGS = (URG,ACK,PSH,RST,SYN,FIN)
    Win = int(trame[28:32],16)
    if(THL != "5"):
        #Option(s) TCP presente
        index = int(THL,16)
        fin_entete = index*8
        data = trame[fin_entete:]
        #TRAITEMENT DES OPTIONS
        option = trame[40:fin_entete]
        b = 0
        MSS, SACK, TSval, TSecr, WS = (0,0,0,0,0)
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
        #CALCUL DE WINDOW
        if(SYN == 0):
            Win = Win*WS
    else:
        data = trame[40:]
    return (HTTP, PortSrc, PortDest, THL, FLAGS, Win, OPT, data)