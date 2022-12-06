from tkinter import *
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox

def interface (IPportsrc, IPportdst, commentaire, nom_fichier="") :
    
    global entetes, ports1, ports2, coms, fleches 
    ports1 = []
    ports2 = []
    coms = []
    fleches = []
    entetes = []
    
    # reinitialise l'interface
    def resetAll() :
        global entetes, ports1, ports2, coms, fleches
        for (p1, p2, c, f) in zip(ports1, ports2,coms, fleches) : 
            p1["text"] = ""
            p2["text"] = ""
            c["text"] = ""
            f["height"] = 0
        for e in entetes :
            e["text"] = ""
            
        entetes = []
        ports1 = []
        ports2 = []
        coms = []
        fleches = []
        
            
    # action de filtrage
    def action(event) :
        global entetes, ports1, ports2, coms, fleches
        
        # récupérer la valeur de la sélection de la liste combobox
        protocole = listeProtocoles.get()
        ipCourrant = listeAdressesIP.get()
        print(ipCourrant)
        resetAll()

        filtreIPportsrc = []
        filtreIPportdst = []
        filtreCom = []
        if(ipCourrant == "Toutes les IP") :
           filtreIPportsrc = IPportsrc
           filtreIPportdst = IPportdst
           filtreCom = commentaire
        else :
            for i in range (len(IPportsrc)) :
                # si la trame contient l'IP filtré
                if (ipCourrant == IPportsrc[i][0] or ipCourrant == IPportdst[i][0]) :
                    filtreCom.append(commentaire[i])
                    filtreIPportsrc.append(IPportsrc[i])
                    filtreIPportdst.append(IPportdst[i])
                    
        # si on veut filtrer par protocole
        if(protocole != "Tous les protocoles") :
            filtreComBouble = []
            filtreIPportsrcBouble = []
            filtreIPportdstBouble = []
            j=0
            for c in filtreCom :
                i = c.find(":")
                if (protocole == c[0:i]) :
                    filtreComBouble.append(c)
                    filtreIPportsrcBouble.append(filtreIPportsrc[j])
                    filtreIPportdstBouble.append(filtreIPportdst[j])
                j += 1
            filtreCom = filtreComBouble
            filtreIPportsrc = filtreIPportsrcBouble
            filtreIPportdst = filtreIPportdstBouble
            
        print (filtreIPportsrc)
        print (filtreIPportdst)
        print (filtreCom)
        filtreIP = nbIP(filtreIPportsrc, IP=[])
        filtreIP = nbIP(filtreIPportdst, filtreIP)
        print(filtreIP)
        
        # mettre en entête les IP et le commentaire
        for i in range (0, len(filtreIP)) :
            entete = Label(fenetre, text = filtreIP[i])
            entetes.append(entete)
            entete.place(x = 10 + 120*i, y = 50)    
        entete = Label(fenetre, text = "Commentaire")
        entetes.append(entete)
        entete.place(x = 10 + 120*len(filtreIP), y = 50)
        
        # place les ports et les commentaires
        indice = 0
        for (i, j) in zip(filtreIPportsrc, filtreIPportdst) :  
            port1 = Label(fenetre, text = i[1])
            ports1.append(port1)
            port1.place(x = 35 + 120*(filtreIP.index(i[0])) , y = 80 + 20*(indice))
            port2 = Label(fenetre, text = j[1])
            ports2.append(port2)
            port2.place(x = 35 + 120*(filtreIP.index(j[0])), y = 80 + 20*(indice))
            com = Label(fenetre, text = filtreCom[indice])
            coms.append(com)
            com.place(x = 10 + 120*(len(filtreIP)), y = 80 + 20*(indice))
            indice += 1
            
            tailleFleche = 120*(filtreIP.index(j[0])) - 120*(filtreIP.index(i[0])) 
            # faire une flèche de taille tailleFleche
            if tailleFleche > 0 :
                tailleFleche -= 40 
                f = Canvas(fenetre, width = tailleFleche, height = 20)
                f.create_line(0, 10, tailleFleche, 10, arrow = LAST)
                fleches.append(f)
                f.place(x = 120*(filtreIP.index(i[0])) + 70, y = 80 + 20*(indice-1))
            else :
                tailleFleche += 40 
                f = Canvas(fenetre, width = -tailleFleche, height = 20)
                f.create_line(-tailleFleche, 10, 0, 10, arrow = LAST)
                fleches.append(f)
                f.place(x = 120*(filtreIP.index(j[0])) + 70, y = 80 + 20*(indice-1))
        
        
    # création d'un fichier texte
    if nom_fichier != "" :
        fichier = open("../../Traces/"+nom_fichier, "w") 
    
    #interface graphique tkinter 
    fenetre = fenetreGraphique()
    
    # on détermine les IP différentes
    IP = nbIP(IPportsrc)
    IP = nbIP(IPportdst, IP)
    print(IP)

    # filtrage 
    listeProtocoles, listeAdressesIP = listeDeroulante(IP, fenetre)
    # lier un événement du type CoboboxSelected
    listeProtocoles.bind("<<ComboboxSelected>>", action)
    listeAdressesIP.bind("<<ComboboxSelected>>", action)
    
    # mettre en entête les IP et le commentaire
    for i in range (0, len(IP)) :
        entete = Label(fenetre, text = IP[i])
        entetes.append(entete)
        entete.place(x = 10 + 120*i, y = 50)    
        fichier.write(IP[i] + "\t\t")   # ecriture dans le fichier texte
    fichier.write("Commentaire\n")      # ecriture dans le fichier texte
    entete = Label(fenetre, text = "Commentaire")
    entetes.append(entete)
    entete.place(x = 10 + 120*len(IP), y = 50)
    
    # place les ports et les commentaires
    indice = 0
    for (i, j) in zip(IPportsrc, IPportdst) :  
        port1 = Label(fenetre, text = i[1])
        ports1.append(port1)
        port1.place(x = 35 + 120*(IP.index(i[0])) , y = 80 + 20*(indice))
        port2 = Label(fenetre, text = j[1])
        ports2.append(port2)
        port2.place(x = 35 + 120*(IP.index(j[0])), y = 80 + 20*(indice))
        com = Label(fenetre, text = commentaire[indice])
        coms.append(com)
        com.place(x = 10 + 120*(len(IP)), y = 80 + 20*(indice))
        indice += 1
        # ecriture dans le fichier texte
        #fichier.write("\t\t\t\t\t"*IP.index(i[0]) + str(i[1]) + "\t\t\t\t\t"*IP.index(j[0]) + str(j[1]) + "                "*(len(IP)) + commentaire[indice] + "\n")
        
        tailleFleche = 120*(IP.index(j[0])) - 120*(IP.index(i[0])) 
        # faire une flèche de taille tailleFleche
        if tailleFleche > 0 :
            tailleFleche -= 40 
            f = Canvas(fenetre, width = tailleFleche, height = 20)
            f.create_line(0, 10, tailleFleche, 10, arrow = LAST)
            fleches.append(f)
            f.place(x = 120*(IP.index(i[0])) + 70, y = 80 + 20*(indice-1))
        else :
            tailleFleche += 40 
            f = Canvas(fenetre, width = -tailleFleche, height = 20)
            f.create_line(-tailleFleche, 10, 0, 10, arrow = LAST)
            fleches.append(f)
            f.place(x = 120*(IP.index(j[0])) + 70, y = 80 + 20*(indice-1))
            
    


    fichier.close()
    
    
    """
    # treeview de len(IP) colonnes
    tree = treeview(IP, fenetre)
    
    # pour que le tableau prenne toute la fenêtre
    tree.pack(fill=BOTH, expand=1)

    # ajout d'une barre de défilement
    scrollbar = Scrollbar(fenetre, orient = "vertical", command=tree.yview)
    scrollbar.place(x = 983, y = 0, height = 600)
    tree.configure(yscrollcommand=scrollbar.set)

    # ajout d'une barre de défilement horizontale
    scrollbar2 = Scrollbar(fenetre, orient = "horizontal", command=tree.xview)
    scrollbar2.place(x = 0, y = 583, width = 983)
    tree.configure(xscrollcommand=scrollbar2.set)
    """
    """
    # ajout d'une trame
    for i in range (0, len(portsrc)):
        # si le port source est le port de IP1
        if(portsrc[i] == portg) :
        # ajouter une  flèche de IP1 vers IP2, avec un commentaire
            tree.insert("", "end", values=(portg[1],"----------------->", portd[1], commentaire[i]))
        else :
        # ajouter une  flèche de IP2 vers IP1, avec un commentaire
            tree.insert("", "end", values=(portg[1],"<-----------------", portd[1], commentaire[i]))
            
    # écriture dans le fichier texte
    fichier.write(portg[0] + "                                                          " + portd[0] + "   Comment\n\n")
    for child in tree.get_children():
        fichier.write(str(tree.item(child)["values"]) + " \n") 
    fichier.close()
    """
    #ouvre l'interface graphique
    fenetre.mainloop()    
    
def fenetreGraphique ():
    fenetre = Tk()
    fenetre.title("Visualisateur de trafic réseau")
    fenetre.geometry("1000x600")
    #+fenetre.resizable(False, False)
    return fenetre

# retourne une liste d'IP
def nbIP(p, IP = []) :
    for e in p :
        print(e)
        if e[0] not in IP :
            IP.append(e[0])
    return IP

def listeDeroulante (IP, fenetre) :
    # Création des listes déroulante
    listeProtocoles = ["Tous les protocoles", "IPv4" , "TCP" , "HTTP"]
    listeAdressesIP = ["Toutes les IP"] + IP
    
    # Création de la Combobox via la méthode ttk.Combobox()
    listeCombo1 = Combobox(fenetre, values=listeProtocoles , width = 24)
    listeCombo2 = Combobox(fenetre, values=listeAdressesIP , width = 24)
    
    # Choisir l'élément qui s'affiche par défaut
    listeCombo1.current(0)
    listeCombo2.current(0)
    listeCombo1.place( x = 10 , y = 10 , width = 150)
    listeCombo2.place( x = 200 , y = 10 , width = 120)
    
    return listeCombo1, listeCombo2