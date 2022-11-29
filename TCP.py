def lectureTCP(trame):
    PortSrc = trame[0:4]
    PortDest = trame[4:8]
    SN = trame[8:16]
    THL = trame[24]
    if(THL != "5"):
        print("Option(s) TCP presente")
        index = int(THL,16)
        fin_entete = index*8
        data = trame[fin_entete:]
    else:
        data = trame[40:]
    return (PortSrc, PortDest, data)