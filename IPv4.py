def lectureIPv4(trame):
    if(trame[28] != 4):
        print("La version de la trame ne correspond pas a IPv4")
        return 
    IHL = trame[29]
    if(IHL > 5):
        print("Option(s) IP presente")
        option = True
    total_length = trame[32:36]
    TTL = trame[44:46]
    protocol = trame[46:48]
    IPSrc = trame[48:56]
    IPDest = trame[56:63]
    if(option):
        RR = trame[63:65]
        if(RR == "07"):
            print("Option Record Route")
    return (option, protocol, IPSrc, IPDest)


