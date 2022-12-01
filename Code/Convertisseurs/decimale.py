def IPv4_dec(ip) :
    return str(int(ip[0:2], 16))\
        +"."+str(int(ip[2:4], 16))\
        +"."+str(int(ip[4:6], 16))\
        +"."+str(int(ip[6:8], 16))

def port_dec(port) :
    return str(int(port,16))