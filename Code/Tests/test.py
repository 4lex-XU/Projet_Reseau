import sys
sys.path.append("..")
from Lecteurs.Ethernet import *
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *

#test
trame = "00 00 00 00 00 00 00 00 00 00 00 00 08 00 45 00 00 3c b9 57 40 00 40 06 83 62 7f 00 00 01 7f 00 00 01 c9 3e ff 98 d7 79 f1 e0 00 00 00 00 a0 02 ff d7 fe 30 00 00 02 04 ff d7 04 02 08 0a 56 2a d7 83 00 00 00 00 01 03 03 0a"
trame = trame.replace(" ","")
e = lectureEthernet(trame)
print(e[0])
print(e[1])
print(e[2])
if(e[2] == "0800"):
    ip = lectureIPv4(trame)
    print(ip[0])
    print(ip[1])
    print(ip[2])
    print(ip[3])
if(ip[1] == "06"):
    index = int(ip[0],16)
    fin_entete_ip = index*8
    #print(fin_entete_ip)
    debut_entete_tcp = 28+fin_entete_ip
    #print(debut_entete_tcp)
    tcp = lectureTCP(trame[debut_entete_tcp:])
    print(tcp[0])
    print(tcp[1])
    print(tcp[2])
