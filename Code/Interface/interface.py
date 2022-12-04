from tkinter import *
from tkinter.ttk import Treeview

def interface (IP1, IP2, commentaire, portsrc, portdst) :
    
    # on détermine le port de IP1 et de IP2
    port1 = portsrc[0]
    port2 = portdst[0]
    
    #interface graphique tkinter 
    fenetre = Tk()
    fenetre.title("Visualisateur de trafic réseau")
    fenetre.geometry("1000x600")
    fenetre.resizable(FALSE, FALSE)
    
    # treeview 3 colonnes
    tree = Treeview(fenetre, columns=(IP1, "flèches", IP2, "Comment"), show="headings")
    tree.column(IP1, width = 100, anchor="e")
    tree.column("flèches", width = 300, anchor="center")
    tree.column(IP2, width = 100, anchor="w")
    tree.column("Comment", width = 500, anchor="w")
    tree.heading(IP1, text= IP1)
    tree.heading("flèches", text = " ")
    tree.heading(IP2, text= IP2)
    tree.heading("Comment", text = "Comment")
    tree.place(x = 0, y = 0)

    # pour que le tableau prenne toute la fenêtre
    tree.pack(fill=BOTH, expand=1)

    # ajout d'une barre de défilement vertical
    scrollbar = Scrollbar(fenetre, orient = "vertical", command=tree.yview)
    scrollbar.place(x = 983, y = 0, height = 600)
    tree.configure(yscrollcommand=scrollbar.set)

    # ajout d'une barre de défilement horizontal
    

    # ajout d'une trame
    for i in range (0, len(portsrc)):
        # si le port source est le port de IP1
        if(portsrc[i] == (IP1, port1)) :
        # ajouter une  flèche de IP1 vers IP2, avec un commentaire
            tree.insert("", "end", values=(port1,"--------------------------------------------------------->", port2, commentaire[i]))
        else :
        # ajouter une  flèche de IP2 vers IP1, avec un commentaire
            tree.insert("", "end", values=(port2,"<---------------------------------------------------------", port1, commentaire[i]))

    #ouvre l'interface graphique
    fenetre.mainloop()    