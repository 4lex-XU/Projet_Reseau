def lectureEthernet(trame):
    macDest = trame[0:12]
    macSrc = trame[12:24]
    type = trame[24:28]
    if(type != "0800"):
        print("Le type ne correspond pas a IP")
        return None
    return (macDest,macSrc,type)
