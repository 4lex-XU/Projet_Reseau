def lectureIPv4(trame):
    if(trame[28] != "4"):
        print("La version de la trame ne correspond pas a IPv4")
        return 
    IHL = trame[29]
    option = False
    if(IHL != "5"):
        print("Option(s) IP presente")
        option = True
    total_length = trame[32:36]
    TTL = trame[44:46]
    protocol = trame[46:48]
    IPSrc = trame[52:60]
    IPDest = trame[60:68]
    if(option):
        RR = trame[68:70]
        if(RR == "07"):
            print("Option Record Route")
    return (IHL, protocol, IPSrc, IPDest)
