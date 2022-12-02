def lectureIPv4(trame):
    if(trame[28] != "4"):
        #La version de la trame ne correspond pas a IPv4
        return (0,0,0,0)
    IHL = trame[29]
    option = False
    if(IHL != "5"):
        #Option(s) IP presente
        option = True
    total_length = trame[32:36]
    TTL = trame[44:46]
    protocol = trame[46:48] # 06 = TCP, 11 = UDP
    IPSrc = trame[52:60]
    IPDest = trame[60:68]
    return (IHL, protocol, IPSrc, IPDest)
