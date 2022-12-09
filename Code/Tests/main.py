import sys
sys.path.append("..")

from Lecteurs.Ethernet import *
from Lecteurs.Frag_TCP import * 
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *
from Lecteurs.HTTP import *
from Lecteurs.trames import *
from Convertisseurs.decimale import *
from Interface.interface import *

# on obtient le tableau des différentes trames
Trames = diviseurDeTrame("../../Trames/"+sys.argv[1])

#declaration des tableaux 
Tab_PortSrc = []
Tab_PortDest = []
Tab_Comment = []

# VARIABLES GLOBALES
data_fragment = 0
data_length = 0
port_prec = 0
SN = 0
AN = 0
#Window Scale / MSS et port des 2 machines
WS1 = 0
WS2 = 0
MSS1 = 0
MSS2 = 0
port1 = 0
port2 = 0
#Fragmentation au niveau TCP
REQUEST = 0
SN_Frag = 0
AN_Frag = 0
port_Frag = 0
data_Frag = 0
Trames_Frag = []
HTTP_Frag = []
premier = TRUE
FRAG = 0

for trame in Trames :
    if(REQUEST == 0):
        FRAG = 0
    #TEST ETHERNET
    if(lectureEthernet(trame) != None):
        MACdst, MACsrc, type = lectureEthernet(trame)
        Comment = "Ethernet: " + MACsrc + " -> " + MACdst + " type = " + type
        if(MAC_dec(MACdst) == "255:255:255:255:255:255"):
            Comment += " [Broadcast]"

        #TEST VERSION IPv4
        if(type != "0800"):
            print("Le type ne correspond pas a IP")
            Comment += " [TYPE DOES'T MATCH IP]"
        elif(lectureIPv4(trame) != None):
            IHL, protocol, IPSrc, IPDest, option, TotalLength, DF, MF, offset, TTL = lectureIPv4(trame)
            Comment = "IPv4: " + IPv4_dec(IPSrc) + " -> " + IPv4_dec(IPDest) + " protocol = " + protocol + " TTL = " + str(TTL)
            if(option):
                Comment += " [Option]"
            else:
                Comment += " [No Option]"
            if(DF == "1"):
                Comment += " [Don't Fragment]"
            if(MF == "1"):
                Comment += " [More Fragment]"
                if(offset == 0):
                    Comment += " Offset = " + str(offset) + " [First fragment]"
                    data_fragment = TotalLength//8
                elif(offset%data_fragment == 0):
                    Comment += " Offset = " + str(offset) + " [Next fragment]"
            elif(data_fragment == 0):
                Comment += " Offset = " + str(offset) + " [No fragment]"
            elif(offset%data_fragment == 0):
                Comment += " Offset = " + str(offset) + " [Last fragment]"
                data_fragment = 0

            #TEST ENTETE TCP
            fin_ip = IHL * 8
            debut_tcp = 28 + fin_ip
            if(protocol != "06"):
                print("Le protocole ne correspond pas a TCP")
                Comment += " [PROTOCOL DOES'T MATCH TCP]"
            elif(lectureTCP(trame[debut_tcp:]) != None):
                HTTP, PortSrc, PortDest, THL, FLAGS, Win, OPT, data = lectureTCP(trame[debut_tcp:])
        
                #PADDING
                if(TotalLength == THL*4):
                    data = ""
            
                #AJOUT DANS LES TABLEAUX DE PORT SOURCE ET DESTINATION 
                Tab_PortSrc.append((IPv4_dec(IPSrc), port_dec(PortSrc)))
                Tab_PortDest.append((IPv4_dec(IPDest), port_dec(PortDest)))

                #VERIFICATION
                CHECKSUM = checksumTCP(IPSrc, IPDest, protocol, THL, PortSrc, PortDest, trame[debut_tcp:])

                debut_http = debut_tcp + THL*8
                #FRAGMENTATION TCP
                if(REQUEST == 1):
                    if(premier):
                        if((port_dec(PortSrc) == port1 and TotalLength-THL*4 >= MSS1) or (port_dec(PortSrc) == port2 and TotalLength-THL*4 >= MSS2)):
                            port_Frag = port_dec(PortSrc)
                            HTTP_Frag = trame[debut_http:]
                            premier = FALSE
                    elif(FLAGS[2] == "1"):
                        if((port_dec(PortSrc) == port1 and TotalLength-THL*4 < MSS1) or (port_dec(PortSrc) == port2 and TotalLength-THL*4 < MSS2)):
                            Comment_bis = fragmentation_tcp(Trames_Frag, SN_Frag, AN_Frag, data_Frag, WS1, WS2, MSS1, MSS2, port1, port2, port_prec, port_Frag)
                            #ECHANGE DE COMMENTAIRE
                            for i in range(len(Trames_Frag)):
                                Tab_Comment[len(Tab_Comment)-len(Trames_Frag)+i] = Comment_bis[i]
                            #TRAME HTTP FRAGMENTE
                            version, code, message, contentType = lectureHTTPrep(HTTP_Frag)
                            Comment_Frag = "HTTP: " + version + " " + code + " " + message + " " + contentType
                            Tab_Comment.append((Comment_Frag, CHECKSUM))
                            FRAG = 1
                            REQUEST = 0
                            SN_Frag = 0
                            AN_Frag = 0
                            port_Frag = 0
                            data_Frag = 0
                            Trames_Frag = []
                            HTTP_Frag = []
                            premier = TRUE
                    Trames_Frag.append(trame)

                #TRAITEMENT DES FLAGS
                flags = "["
                if(FLAGS[0] == "1"):
                    flags += " URG"
                if(FLAGS[1] == "1"):
                    flags += " ACK"
                if(FLAGS[2] == "1"):
                    flags += " PSH"
                if(FLAGS[3] == "1"):
                    flags += " RST"
                if(FLAGS[4] == "1"):
                    flags += " SYN"
                if(FLAGS[5] == "1"):
                    flags += " FIN"
                flags += " ]"

                #SYN
                if(FLAGS == ("0","0","0","0","1","0")):
                    port1 = port_dec(PortSrc)
                    MSS1 = OPT[0]
                    WS1 = OPT[4]
                    data_length = 0
                    SN = 0
                    AN = 0
                    flags += " SN = " + str(SN)
                #SYN/ACK
                if(FLAGS == ("0","1","0","0","1","0")):
                    port2 = port_dec(PortSrc)
                    MSS2 = OPT[0]
                    WS2 = OPT[4]
                    AN = SN+1
                    flags += " SN = " + str(SN) + " AN = " + str(AN)
                    SN += 1
                #ACK
                if(FLAGS == ("0","1","0","0","0","0")):
                    if(port_prec == port_dec(PortSrc)):
                        SN = SN+data_length
                        flags += " SN = " + str(SN) + " AN = " + str(AN)
                    else:
                        tmp = SN
                        SN = AN
                        AN = tmp+data_length
                        flags += " SN = " + str(SN) + " AN = " + str(AN)
                #PUSH/ACK
                if(FLAGS == ("0","1","1","0","0","0")):
                    if(port_prec == port_dec(PortSrc)):
                        SN = SN+data_length
                        flags += " SN = " + str(SN) + " AN = " + str(AN)
                    else:
                        tmp = SN
                        SN = AN
                        AN = tmp+data_length
                        flags += " SN = " + str(SN) + " AN = " + str(AN)
                
                data_length = len(data)//2

                #FIN
                if(FLAGS == ("0","0","0","0","0","1")):
                    SN = SN+data_length
                    flags += " SN = " + str(SN) + " AN = " + str(AN)
                    SN += 1
                #FIN/ACK
                if(FLAGS == ("0","1","0","0","0","1")):
                    if(port_prec == port_dec(PortSrc)):
                        SN = SN+data_length
                        flags += " SN = " + str(SN) + " AN = " + str(AN)
                        SN += 1
                    else:
                        tmp = SN
                        SN = AN
                        AN = tmp+data_length
                        flags += " SN = " + str(SN) + " AN = " + str(AN)
                        SN += 1
                port_prec = port_dec(PortSrc)

                #TEST HTTP
                if((HTTP == -1) or (TotalLength == THL*4)):
                    Comment = "TCP: " + port_dec(PortSrc) + " -> " + port_dec(PortDest) + " " + flags
                    
                    #CALCUL DE WINDOW
                    if(FLAGS[4] == "0"):
                        if(port1 == port_dec(PortSrc)):
                            Win = Win*WS1
                        elif(port2 == port_dec(PortSrc)):
                            Win = Win*WS2

                    Comment += " Win = " + str(Win) + " Data_length = " + str((len(data))//2) 
                    if(OPT[0] != 0):
                        Comment += " MSS = " + str(OPT[0])
                    
                    #SACK Permitted
                    if(OPT[1] == 1):
                        Comment += " SACK_PERM"

                    Comment += " TSval = " + str(OPT[2]) + " TSecr = " + str(OPT[3]) + " WS = " + str(OPT[4])
                
                elif(HTTP == 0 and FRAG == 0): #REQUEST
                    if(lectureHTTPreq(trame[debut_http:]) != None):
                        methode, contenu = lectureHTTPreq(trame[debut_http:])
                        Comment = "HTTP: " + methode + " " + contenu
                        if(FRAG == 0):
                            REQUEST = 1
                            SN_Frag = SN
                            AN_Frag = AN
                            data_Frag = data_length
                elif (FRAG == 0): #REPLY
                    if(lectureHTTPrep(trame[debut_http:]) != None):
                        version, code, message, contentType = lectureHTTPrep(trame[debut_http:])
                        Comment = "HTTP: " + version + " " + code + " " + message + " " + contentType
        #AJOUT DU COMMENTAIRE DANS LE TABLEAU
        if(FRAG == 0):
            Tab_Comment.append((Comment, CHECKSUM))
            #print(Comment)
#print(Tab_PortSrc)
#print(Tab_PortDest)
#print(Tab_Comment)
interface (Tab_PortSrc, Tab_PortDest, Tab_Comment, sys.argv[2])