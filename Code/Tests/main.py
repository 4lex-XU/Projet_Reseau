import sys
sys.path.append("..")
from Lecteurs.Ethernet import *
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *
from Lecteurs.trames import *
from Convertisseurs.decimale import *

# on obtient le tableau des différentes trames
trames = diviseurDeTrame("../../Trames/tcp.txt")

for trame in trames :
    MACdst, MACsrc, type = lectureEthernet(trame)
    #si type ip
    if(type == "0800") :
        IHL, protocol, IPSrc, IPDest = lectureIPv4(trame)
        if(protocol == "06") :
            indice = int(IHL,16)
            fin_ip = indice * 8
            debut_tcp = 28 + fin_ip
            PortSrc, PortDest, data = lectureTCP(trame[debut_tcp:])
            print("Port Source : ", int(PortSrc,16))
            print("Port Destinataire : ",int(PortDest,16))
            print(data)
