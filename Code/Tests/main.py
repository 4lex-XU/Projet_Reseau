import sys
sys.path.append("..")
from Lecteurs.Ethernet import *
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *
from Lecteurs.HTTP import *
from Lecteurs.trames import *
from Convertisseurs.decimale import *
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

trame_rep = "48 54 54 50 2f 31 2e 31 20 32 30 30 20 4f 4b 0d   0a 44 61 74 65 3a 20 46 72 69 2c 20 30 32 20 44  65 63 20 32 30 32 32 20 32 30 3a 31 35 3a 35 31  20 47 4d 54 0d 0a 53 65 72 76 65 72 3a 20 41 70 61 63 68 65 2f 32 2e 30 2e 35 34 20 28 4f 6d 690050   63 72 6f 6e 20 57 65 62 2d 53 65 72 76 69 63 650060   73 29 0d 0a 4c 61 73 74 2d 4d 6f 64 69 66 69 650070   64 3a 20 54 75 65 2c 20 31 31 20 53 65 70 20 320080   30 31 38 20 31 35 3a 31 32 3a 31 37 20 47 4d 540090   0d 0a 45 54 61 67 3a 20 22 39 61 63 32 61 61 2d00a0   32 61 65 65 2d 65 36 34 30 62 36 34 30 22 0d 0a00b0   41 63 63 65 70 74 2d 52 61 6e 67 65 73 3a 20 6200c0   79 74 65 73 0d 0a 43 6f 6e 74 65 6e 74 2d 4c 6500d0   6e 67 74 68 3a 20 31 30 39 39 30 0d 0a 43 6f 6e00e0   6e 65 63 74 69 6f 6e 3a 20 63 6c 6f 73 65 0d 0a00f0   43 6f 6e 74 65 6e 74 2d 54 79 70 65 3a 20 74 650100   78 74 2f 68 74 6d 6c 0d 0a 0d 0a"
trame_rep = trame_rep.replace(" ","")
print(lectureHTTPrep(trame_rep))