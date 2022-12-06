def hexaToBinary(hexa):
    #Conversion binaire
    binaire = ""
    for i in hexa:
        hexa_to_dec = int(i,16)
        binaire += bin(hexa_to_dec)[2:].zfill(4)
    return binaire