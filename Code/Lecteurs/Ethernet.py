def lectureEthernet(trame):
    #Trame vide
    if(trame is None):
        print("Trame vide")
        return None
    macDest = trame[0:12]
    macSrc = trame[12:24]
    type = trame[24:28]
    return (macDest,macSrc,type)
