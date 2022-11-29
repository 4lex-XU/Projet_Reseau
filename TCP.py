def lectureTCP(trame):
    PortSrc = trame[0:4]
    PortDest = trame[4:8]
    SN = trame[8:16]
    THL = trame[16]
    if(THL > 5):
        print("Option(s) IP presente")
        option = True
        data = trame[60:]
    else:
        data = trame[20:]
    return (PortSrc, PortDest, data)