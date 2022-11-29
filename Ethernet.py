def lectureEthernet(trame):
    macDest = trame[0:12]
    macSrc = trame[12:24]
    type = trame[24:28]
    return (macDest,macSrc,type)
