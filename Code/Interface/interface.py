from tkinter import *
from tkinter.ttk import Treeview
from tkinter.ttk import Combobox


def interface (IPportsrc, IPportdst, commentaire, nom_fichier="") :
    
    # action de filtrage
    def action(event) :
        global entetes, ports1, ports2, coms, fleches
        
        # récupérer la valeur de la sélection de la liste combobox
        protocole = listeProtocoles.get()
        ipCourrant = listeAdressesIP.get()
        
        # réinitialiser le canvas
        canvas.delete("all")
        
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
                i = c[0].find(":")
                if (protocole == c[0][0:i]) :
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
            entete = Label(canvas, text = filtreIP[i])
            canvas.create_window(10 + 120*i, 50, anchor=NW, window=entete)
        entete = Label(canvas, text = "Commentaire")
        canvas.create_window(10 + 120*len(filtreIP), 50, anchor=NW, window=entete)
        
        # place les ports et les commentaires
        indice = 0
        for (i, j) in zip(filtreIPportsrc, filtreIPportdst) :  
            port1 = Label(canvas, text = i[1])
            canvas.create_window(35 + 120*(filtreIP.index(i[0])), 80 + 20*(indice), anchor=NW, window=port1)
            port2 = Label(canvas, text = j[1])
            canvas.create_window(35 + 120*(filtreIP.index(j[0])), 80 + 20*(indice), anchor=NW, window=port2)
            com = Label(canvas, text = filtreCom[indice][0])
            canvas.create_window(10 + 120*(len(filtreIP)), 80 + 20*(indice), anchor=NW, window=com)
            indice += 1
            
            tailleFleche = 120*(filtreIP.index(j[0])) - 120*(filtreIP.index(i[0])) 
            # faire une flèche de taille tailleFleche
            if tailleFleche > 0 :
                tailleFleche -= 40 
                f = Canvas(canvas, width = tailleFleche, height = 20)
                f.create_line(0, 10, tailleFleche, 10, arrow = LAST)
                canvas.create_window(120*(filtreIP.index(i[0])) + 70, 80 + 20*(indice-1), anchor=NW, window=f)
            else :
                tailleFleche += 40 
                f = Canvas(canvas, width = -tailleFleche, height = 20)
                f.create_line(-tailleFleche, 10, 0, 10, arrow = LAST)
                canvas.create_window(120*(filtreIP.index(j[0])) + 70, 80 + 20*(indice-1), anchor=NW, window=f)
        
        
    # création d'un fichier texte
    if nom_fichier != "" :
        fichier = open("../../Traces/"+nom_fichier, "w") 
    
    #interface graphique tkinter 
    fenetre = fenetreGraphique()
   
    # creer une frame
    frame = Frame(fenetre, width = 1000, height = 1000, bg = "white")
    frame.pack(expand=True, fill=BOTH)
    
    # creer un canvas
    canvas = Canvas(frame, width = 1000, height = 1000, scrollregion=(0,0,30000,30000))
    hbar = Scrollbar(frame, orient=HORIZONTAL)
    hbar.pack(side=BOTTOM, fill=X)
    hbar.config(command=canvas.xview)
    vbar = Scrollbar(frame, orient=VERTICAL)
    vbar.pack(side=RIGHT, fill=Y)
    vbar.config(command=canvas.yview)
    canvas.config(width=1000, height=1000)
    canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
    canvas.pack(side=LEFT,expand=True,fill=BOTH)
    
    # on détermine les IP différentes
    IP = nbIP(IPportsrc)
    IP = nbIP(IPportdst, IP)

    # filtrage 
    listeProtocoles, listeAdressesIP = listeDeroulante(IP, fenetre)
    # lier un événement du type CoboboxSelected
    listeProtocoles.bind("<<ComboboxSelected>>", action)
    listeAdressesIP.bind("<<ComboboxSelected>>", action)
    
    # mettre en entête les IP et le commentaire
    for i in range (0, len(IP)) :
        entete = Label(canvas, text = IP[i])
        canvas.create_window(10 + 120*i, 50, anchor=NW, window=entete)  
        #fichier.write(IP[i] + "\t\t")   # ecriture dans le fichier texte
    #fichier.write("Commentaire\n")      # ecriture dans le fichier texte
    entete = Label(canvas, text = "Commentaire")
    canvas.create_window(10 + 120*len(IP), 50, anchor=NW, window=entete)
    
    # place les ports et les commentaires
    indice = 0
    for (i, j) in zip(IPportsrc, IPportdst) :  
        port1 = Label(canvas, text = i[1])
        canvas.create_window(35 + 120*(IP.index(i[0])) , 80 + 20*(indice), anchor=NW, window=port1)
        port2 = Label(canvas, text = j[1])
        canvas.create_window(35 + 120*(IP.index(j[0])), 80 + 20*(indice), anchor=NW, window=port2)
        com = Label(canvas, text = commentaire[indice][0])
        canvas.create_window(10 + 120*(len(IP)), 80 + 20*(indice), anchor=NW, window=com)
        indice += 1
        # ecriture dans le fichier texte
        #fichier.write("\t\t\t\t\t"*IP.index(i[0]) + str(i[1]) + "\t\t\t\t\t"*IP.index(j[0]) + str(j[1]) + "                "*(len(IP)) + commentaire[indice] + "\n")
        
        tailleFleche = 120*(IP.index(j[0])) - 120*(IP.index(i[0])) 
        # faire une flèche de taille tailleFleche
        if tailleFleche > 0 :
            tailleFleche -= 40 
            f = Canvas(canvas, width = tailleFleche, height = 20)
            f.create_line(0, 10, tailleFleche, 10, arrow = LAST)
            canvas.create_window(120*(IP.index(i[0])) + 70, 80 + 20*(indice-1), anchor=NW, window=f)
        else :
            tailleFleche += 40 
            f = Canvas(canvas, width = -tailleFleche, height = 20)
            f.create_line(-tailleFleche, 10, 0, 10, arrow = LAST)
            canvas.create_window(120*(IP.index(j[0])) + 70, 80 + 20*(indice-1), anchor=NW, window=f)
            
    fichier.close()
    
    #ouvre l'interface graphique
    fenetre.mainloop()    
    
def fenetreGraphique ():
    fenetre = Tk()
    fenetre.title("Visualisateur de trafic réseau")
    fenetre.geometry("1000x600")
    #fenetre.resizable(False, False)
    return fenetre

# retourne une liste d'IP
def nbIP(p, IP = []) :
    for e in p :
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