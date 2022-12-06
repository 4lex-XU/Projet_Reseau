import sys
sys.path.append("..")

from Lecteurs.Ethernet import *
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
SN = 0
AN = 0
#Window Scale et port des 2 machines
WS1 = 0
WS2 = 0
port1 = 0
port2 = 0

for trame in Trames :
    #TEST ETHERNET
    if(lectureEthernet(trame) != None):
        MACdst, MACsrc, type = lectureEthernet(trame)
        
        #Comment = "Ethernet: " + MACsrc + " -> " + MACdst + " type = " + type
        #if(MAC_dec(MACdst) == "255:255:255:255:255:255"):
        #    Comment += " [Broadcast]"

        #TEST VERSION IPv4
        if(type != "0800"):
            print("Le type ne correspond pas a IP")
        elif(lectureIPv4(trame) != None):
            IHL, protocol, IPSrc, IPDest, option, TotalLength, DF, MF, offset, TTL = lectureIPv4(trame)
            Comment = "IPv4: " + IPv4_dec(IPSrc) + " -> " + IPv4_dec(IPDest) + " protocol = " + protocol + " TTL = " + TTL
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
            elif(lectureTCP(trame[debut_tcp:]) != None):
                HTTP, PortSrc, PortDest, THL, FLAGS, Win, OPT, data = lectureTCP(trame[debut_tcp:])

                #AJOUT DANS LES TABLEAUX DE PORT SOURCE ET DESTINATION 
                Tab_PortSrc.append((IPv4_dec(IPSrc), port_dec(PortSrc)))
                Tab_PortDest.append((IPv4_dec(IPDest), port_dec(PortDest)))

                #TEST HTTP
                if(HTTP == -1):
                    Comment = "TCP: " + port_dec(PortSrc) + " -> " + port_dec(PortDest)
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
                    Comment += " " + flags
                    #TRAITEMENT DES FLAGS
                    #SYN
                    if(FLAGS == ("0","0","0","0","1","0")):
                        port1 = port_dec(PortSrc)
                        WS1 = OPT[4]
                        data_length = 0
                        SN = 0
                        AN = 0
                        Comment += " SN = " + str(SN)
                    #SYN/ACK
                    if(FLAGS == ("0","1","0","0","1","0")):
                        port2 = port_dec(PortSrc)
                        WS2 = OPT[4]
                        AN = SN+1
                        Comment += " SN = " + str(SN) + " AN = " + str(AN)
                        SN += 1
                    #ACK
                    if(FLAGS == ("0","1","0","0","0","0")):
                        tmp = SN
                        SN = AN
                        AN = tmp+data_length
                        Comment += " SN = " + str(SN) + " AN = " + str(AN)
                    #PUSH/ACK
                    if(FLAGS == ("0","1","1","0","0","0")):
                        SN = SN+data_length
                        Comment += " SN = " + str(SN) + " AN = " + str(AN)
                    
                    data_length = len(data)//2

                    #FIN
                    if(FLAGS == ("0","0","0","0","0","1")):
                        SN = SN+data_length
                        Comment += " SN = " + str(SN) + " AN = " + str(AN)
                        SN += 1
                    #FIN/ACK
                    if(FLAGS == ("0","1","0","0","0","1")):
                        tmp = SN
                        SN = AN
                        AN = tmp
                        Comment += " SN = " + str(SN) + " AN = " + str(AN)
                        SN += 1
                    
                    #CALCUL DE WINDOW
                    if(FLAGS[4] == "0"):
                        if(port1 == port_dec(PortSrc)):
                            Win = Win*WS1
                        elif(port2 == port_dec(PortSrc)):
                            Win = Win*WS2

                    Comment += " Win = " + str(Win) + " Data_length = " + str((len(data))//2) + " MSS = " + str(OPT[0])
                    
                    #SACK Permitted
                    if(OPT[1] == 1):
                        Comment += " SACK_PERM"

                    Comment += " TSval = " + str(OPT[2]) + " TSecr = " + str(OPT[3]) + " WS = " + str(OPT[4])

                elif(HTTP == 0): #REQUEST
                    if(lectureHTTPreq(trame[THL:]) != None):
                        methode, contenu = lectureHTTPreq(trame[THL:])
                        Comment = "HTTP: " + methode + " " + contenu
                else: #REPLY
                    if(lectureHTTPrep(trame[THL:]) != None):
                        version, code, message = lectureHTTPrep(trame[THL:])
                        Comment = "HTTP: " + version + " " + code + " " + message
            #AJOUT DU COMMENTAIRE DANS LE TABLEAU
            print(Comment)
            Tab_Comment.append(Comment)

#print(Tab_PortSrc)
#print(Tab_PortDest)
#print(Tab_Comment)
#interface (IPv4_dec(IPSrc), IPv4_dec(IPDest), Tab_Comment, Tab_PortSrc, Tab_PortDest)