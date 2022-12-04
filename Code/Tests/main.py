import sys
sys.path.append("..")
from Lecteurs.Ethernet import *
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *
from Lecteurs.HTTP import *
from Lecteurs.trames import *
from Convertisseurs.decimale import *
from Interface.interface import *


"""
# on obtient le tableau des différentes trames
Trames = diviseurDeTrame("../../Trames/tcp.txt")

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
                print("Port Source : ", int(PortSrc,16))
                print("Port Destinataire : ",int(PortDest,16))
                print(data)

"""