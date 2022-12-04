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
data_length = 0
SN = 0
AN = 0
WS = 0

for trame in Trames :
    #TEST TYPE IP
    if(lectureEthernet(trame) != None):
        MACdst, MACsrc, type = lectureEthernet(trame)
        #TEST VERSION IPv4 ET TCP
        if(lectureIPv4(trame) != None):
            IHL, protocol, IPSrc, IPDest = lectureIPv4(trame)
            indice = int(IHL,16)
            fin_ip = indice * 8
            debut_tcp = 28 + fin_ip
            HTTP, PortSrc, PortDest, THL, FLAGS, Win, OPT, data = lectureTCP(trame[debut_tcp:])

            #AJOUT DANS LES TABLEAUX DE PORT SOURCE ET DESTINATION 
            Tab_PortSrc.append((IPv4_dec(IPSrc), port_dec(PortSrc)))
            Tab_PortDest.append((IPv4_dec(IPDest), port_dec(PortDest)))

            Comment = ""
            #TEST HTTP
            if(HTTP == -1):
                Comment = port_dec(PortSrc) + " -> " + port_dec(PortDest)
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
                    WS = OPT[4]
                    data_length = 0
                    SN = 0
                    AN = 0
                    Comment += " SN = " + str(SN)
                #SYN/ACK
                if(FLAGS == ("0","1","0","0","1","0")):
                    WS = OPT[4]
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
                    Win = Win*WS

                Comment += " Win = " + str(Win) + " Data_length = " + str((len(data))//2) + " MSS = " + str(OPT[0])
                
                #SACK Permitted
                if(OPT[1] == 1):
                    Comment += " SACK_PERM"

                Comment += " TSval = " + str(OPT[2]) + " TSecr = " + str(OPT[3]) + " WS = " + str(OPT[4])

            elif(HTTP == 0): #REQUEST
                methode, contenu = lectureHTTPreq(trame[THL:])
                Comment = "HTTP: " + methode + " " + contenu
            else: #REPLY
                version, code, message = lectureHTTPrep(trame[THL:])
                Comment = "HTTP: " + version + " " + code + " " + message
            #AJOUT DU COMMENTAIRE DANS LE TABLEAU
            print(Comment)
            Tab_Comment.append(Comment)

#print(Tab_PortSrc)
#print(Tab_PortDest)
#print(Tab_Comment)
#interface (IPv4_dec(IPSrc), IPv4_dec(IPDest), Tab_Comment, Tab_PortSrc, Tab_PortDest)