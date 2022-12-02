def hexaToASCII(hexa):
    if (len(hexa)%2 != 0) :
        print("Erreur : la chaine de caractères hexadécimaux doit être de longueur paire")
        return None
    else :
        ascii = ""
        for i in range(0,len(hexa),2):
            ascii += chr(int(hexa[i:i+2],16))
        return ascii