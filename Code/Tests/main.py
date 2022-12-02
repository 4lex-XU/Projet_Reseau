import sys
sys.path.append("..")
from Lecteurs.Ethernet import *
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *
from Lecteurs.HTTP import *
from Lecteurs.trames import *
from Convertisseurs.decimale import *

# on obtient le tableau des différentes trames
Trames = diviseurDeTrame("../../Trames/tcp.txt")
data_length = 0
SN = 0
AN = 0

for trame in Trames :
    MACdst, MACsrc, type = lectureEthernet(trame)
    #TEST IPv4
    if(type == "0800") :
        IHL, protocol, IPSrc, IPDest = lectureIPv4(trame)
        if(IHL != 0):
            #TEST TCP
            if(protocol == "06") :
                indice = int(IHL,16)
                fin_ip = indice * 8
                debut_tcp = 28 + fin_ip
                HTTP, PortSrc, PortDest, THL, FLAGS, Win, OPT, data = lectureTCP(trame[debut_tcp:])
                Info = "" + int(PortSrc,16) + " -> " + int(PortDest,16)
                flags = "["
                if(FLAGS[0] == 1):
                    flags += " URG"
                if(FLAGS[1] == 1):
                    flags += " ACK"
                if(FLAGS[2] == 1):
                    flags += " PSH"
                if(FLAGS[3] == 1):
                    flags += " RST"
                if(FLAGS[4] == 1):
                    flags += " SYN"
                if(FLAGS[5] == 1):
                    flags += " FIN"
                flags += " ]"
                Info += " " + flags
                #SYN
                if(FLAGS == (0,0,0,0,1,0)):
                    Info += " SN = " + SN
                if(FLAGS == (0,1,0,0,1,0)):
                    Info += " SN = 0 AN = 1"
                if(FLAGS == (0,1,0,0,0,0)):
                    Info += "SN = 1 AN = 1" 

                
                

                print(data)
