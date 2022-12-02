import sys
sys.path.append("..")
from Lecteurs.Ethernet import *
from Lecteurs.IPv4 import *
from Lecteurs.TCP import *
from Lecteurs.HTTP import *
"""
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
    print(tcp[3])
    print(tcp[4])
    print(tcp[5])
    print(tcp[6])
    print(tcp[7])
"""

trame = " 47 45 54 20 2f 53 70 65 63 6966 69 63 61 74 69 6f 6e 73 2f 61 73 63 69 69 2e68 74 6d 20 48 54 54 50 2f 31 2e 31 0d 0a 48 6f73 74 3a 20 77 77 77 2e 67 6f 6d 61 72 6f 2e 6368 0d 0a 43 6f 6e 6e 65 63 74 69 6f 6e 3a 20 6b 65 65 70 2d 61 6c 69 76 65 0d 0a 55 73 65 72 2d41 67 65 6e 74 3a 20 4d 6f 7a 69 6c 6c 61 2f 35  2e 30 20 28 57 69 6e 64 6f 77 73 20 4e 54 20 31 30 2e 30 3b 20 57 69 6e 36 34 3b 20 78 36 34 29 20 41 70 70 6c 65 57 65 62 4b 69 74 2f 35 33 37 2e 33 36 20 28 4b 48 54 4d 4c 2c 20 6c 69 6b 6520 47 65 63 6b 6f 29 20 43 68 72 6f 6d 65 2f 3130 38 2e 30 2e 30 2e 30 20 53 61 66 61 72 69 2f35 33 37 2e 33 36 0d 0a 41 63 63 65 70 74 3a 202a 2f 2a 0d 0a 53 65 63 2d 47 50 43 3a 20 31 0d0a 41 63 63 65 70 74 2d 4c 61 6e 67 75 61 67 653a 20 66 72 2d 46 52 2c 66 72 0d 0a 41 63 63 6570 74 2d 45 6e 63 6f 64 69 6e 67 3a 20 67 7a 6970 2c 20 64 65 66 6c 61 74 65 0d 0a 0d 0a"
trame = trame.replace(" ","")
print(lectureHTTPreq(trame))

trame_rep = "48 54 54 50 2f 31 2e 31 20 32 30 30 20 4f 4b 0d   0a 44 61 74 65 3a 20 46 72 69 2c 20 30 32 20 44  65 63 20 32 30 32 32 20 32 30 3a 31 35 3a 35 31  20 47 4d 54 0d 0a 53 65 72 76 65 72 3a 20 41 70 61 63 68 65 2f 32 2e 30 2e 35 34 20 28 4f 6d 690050   63 72 6f 6e 20 57 65 62 2d 53 65 72 76 69 63 650060   73 29 0d 0a 4c 61 73 74 2d 4d 6f 64 69 66 69 650070   64 3a 20 54 75 65 2c 20 31 31 20 53 65 70 20 320080   30 31 38 20 31 35 3a 31 32 3a 31 37 20 47 4d 540090   0d 0a 45 54 61 67 3a 20 22 39 61 63 32 61 61 2d00a0   32 61 65 65 2d 65 36 34 30 62 36 34 30 22 0d 0a00b0   41 63 63 65 70 74 2d 52 61 6e 67 65 73 3a 20 6200c0   79 74 65 73 0d 0a 43 6f 6e 74 65 6e 74 2d 4c 6500d0   6e 67 74 68 3a 20 31 30 39 39 30 0d 0a 43 6f 6e00e0   6e 65 63 74 69 6f 6e 3a 20 63 6c 6f 73 65 0d 0a00f0   43 6f 6e 74 65 6e 74 2d 54 79 70 65 3a 20 74 650100   78 74 2f 68 74 6d 6c 0d 0a 0d 0a"
trame_rep = trame_rep.replace(" ","")
print(lectureHTTPrep(trame_rep))
