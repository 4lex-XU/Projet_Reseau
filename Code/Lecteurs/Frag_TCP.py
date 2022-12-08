import sys
sys.path.append("..")

from Lecteurs.Ethernet import *
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *
from Lecteurs.HTTP import *
from Lecteurs.trames import *
from Convertisseurs.decimale import *
from Interface.interface import *

#declaration des tableaux 
Tab_Comment = []

def fragmentation_tcp(Trames, SN, AN, data_length, WS1, WS2, port1, port2, port_prec, port_Frag):
    for trame in Trames :
        #TEST ETHERNET
        if(lectureEthernet(trame) != None):
            MACdst, MACsrc, type = lectureEthernet(trame)

             #TEST VERSION IPv4
            if(type != "0800"):
                print("Le type ne correspond pas a IP")
            elif(lectureIPv4(trame) != None):
                IHL, protocol, IPSrc, IPDest, option, TotalLength, DF, MF, offset, TTL = lectureIPv4(trame)

                #TEST ENTETE TCP
                fin_ip = IHL * 8
                debut_tcp = 28 + fin_ip
                if(protocol != "06"):
                    print("Le protocole ne correspond pas a TCP")
                elif(lectureTCP(trame[debut_tcp:]) != None):
                    HTTP, PortSrc, PortDest, THL, FLAGS, Win, OPT, data = lectureTCP(trame[debut_tcp:])
                    #VERIFICATION
                    CHECKSUM = checksumTCP(IPSrc, IPDest, protocol, THL, PortSrc, PortDest, trame[debut_tcp:])
                    #TRAITEMENT DES FLAGS
                    flags = "[ ACK ]"
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
                    
                    data_length = len(data)//2
                    port_prec = port_dec(PortSrc)
                    
                    #COMMENTAIRE
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
                    if(port_Frag == port_dec(PortSrc)):
                        Comment += " [TCP segment of a reassembled PDU]"
                    
            #AJOUT DU COMMENTAIRE DANS LE TABLEAU
            Tab_Comment.append((Comment, CHECKSUM))
    return Tab_Comment