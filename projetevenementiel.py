import os
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import time

root=tk.Tk()
root.title(" Explorateur de fichier")
favoris=set()
chemin_actuel = os.getcwd()
affichage_favoris = False  

#definition des différents filtres
filtres = {
    "Tous les fichiers": "*",
    "Fichiers texte (*.txt)": ".txt",
    "Images (*.jpg, *.png, *.gif)": (".jpg", ".png", ".gif"),
    "Fichiers Python (*.py)": ".py",
}

filtre_selectionne = StringVar()
filtre_selectionne.set("Tous les fichiers")

# Importation des icones de dossiers et fichiers téléchargées ultérieurement
icon_folder = ImageTk.PhotoImage(Image.open("C:/Users/USER/Desktop/p evenementiel/icons/folder.JPEG").resize((20, 20)))
icon_file = ImageTk.PhotoImage(Image.open("C:/Users/USER/Desktop/p evenementiel/icons/file.PNG").resize((20, 20)))

#Fonction pour le detail des dossiers
def afficher_details(nom):
    # Vérifier si le fichier existe toujours
    if not os.path.exists(nom):  
        messagebox.showerror("Erreur", "Fichier introuvable !")
        return
    
    # Création du frame dans lequel les details vont s'afficher 
    frame_details=tk.Frame(root,borderwidth=2, relief="ridge")
    frame_details.grid(row=3, column=0, padx=5, pady=5, sticky="nsew")

    # Supprimer les anciens widgets
    for widget in frame_details.winfo_children():
        widget.destroy()

    # Récupérer les informations du fichier
    taille = os.path.getsize(nom)  
    taille_str = f"{taille} octets" if taille < 1024 else f"{taille // 1024} Ko"
    date_creation = os.path.getctime(nom)  
    date_modif = os.path.getmtime(nom)  

    # Afficher les différents details
    tk.Label(frame_details, text=f"Nom : {nom}", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=2)
    tk.Label(frame_details, text=f"Taille : {taille_str}").pack(anchor="w", padx=10, pady=2)
    tk.Label(frame_details, text=f"Créé le : {time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(date_creation))}").pack(anchor="w", padx=10, pady=2)
    tk.Label(frame_details, text=f"Modifié le : {time.strftime('%d/%m/%Y %H:%M:%S', time.localtime(date_modif))}").pack(anchor="w", padx=10, pady=2)
#definition de la fonction pour les icones
def icone():
    chemin = os.getcwd()
    elements = os.listdir(chemin)

    for widget in frame3.winfo_children():
        widget.destroy()

    col = 0  # Définir la colonne de départ
    row = 0  # Définir la ligne de départ
    max_columns = 8  # Nombre d'icônes par ligne (modifiable)

    for fichier in elements:
        is_folder = os.path.isdir(fichier)
        icon = icon_folder if is_folder else icon_file

        # Création du Label contenant l'icône
        label_icon = ttk.Label(frame3, image=icon, cursor="hand2")
        label_icon.grid(row=row, column=col, padx=10, pady=5)  
        # Rendre l'icône cliquable
        label_icon.bind("<Double-1>", lambda event, nom=fichier: ouvrir(nom))

        # Création du Label pour le texte (nom du fichier/dossier)
        label_nom = ttk.Label(frame3, text=fichier, anchor="center")
        label_nom.grid(row=row + 1, column=col, padx=10, pady=2)  # Aligner sous l'icône

        # Rendre le texte aussi cliquable
        label_nom.bind("<Double-1>", lambda event, nom=fichier: ouvrir(nom))

        # Passer à la colonne suivante
        col += 1

        # Si le nombre de colonnes atteint le maximum, passer à la ligne suivante
        if col >= max_columns:
            col = 0  
            row += 2  


#Definition de la fonction pour la liste des fichiers
def contenu(filtre=""):
      chemin=os.getcwd()
      fichiers=os.listdir(chemin)
      filtre_actuel = filtres[filtre_selectionne.get()]
      for widget in frame1.winfo_children():
        widget.destroy()
      for fichier in fichiers:
            
            if filtre_actuel == "*" or (isinstance(filtre_actuel, tuple) and fichier.endswith(filtre_actuel)) or fichier.endswith(filtre_actuel):
                  label=ttk.Label(frame1, text=fichier)
                  label.grid(sticky=(S,W))
                  label.bind("<Button-1>", lambda event, lbl=label: surbrillance(lbl))
                  label.bind("<Double-1>", lambda event, nom=fichier: naviguer_dossier(nom))
                  menu = tk.Menu(root, tearoff=0)
                  # Création des différents options du menu
                  menu.add_command(label="Ouvrir", command=lambda nom=fichier: ouvrir(nom))
                  menu.add_command(label="Renommer", command=lambda nom=fichier: renommer(nom))
                  menu.add_command(label="Supprimer", command=lambda nom=fichier: supprimer(nom))
                  menu.add_command(label="Ajouter aux Favoris", command=lambda nom=fichier: ajouter_favori(nom))
                  menu.add_command(label="Details", command=lambda nom=fichier: afficher_details(nom))
                  label.bind("<Button-3>", lambda event, m=menu: afficher_menu(event, m))
                  
 #Fonction pour ajouter aux favoris                 
def ajouter_favori(nom):
    if nom not in favoris:
        favoris.add(nom)
    else:
        messagebox.showinfo("Favoris", f"'{nom}' est déjà dans les favoris.")

#Fonction pour afficher les favoris
def afficher_favoris():
    for widget in frame3.winfo_children():
        widget.destroy()

    ttk.Label(frame3, text="Favoris :", font=("Arial", 10, "bold")).grid(sticky=(S), padx=5, pady=2)

    for fav in favoris:
        label_fav = ttk.Label(frame3, text=fav, fg="orange", cursor="hand2")
        label_fav.grid(sticky=(S), padx=10)
        label_fav.bind("<Double-1>", lambda event, nom=fav: ouvrir(nom))
        
#Definition de la fonction pour le filtre
def changer_filtre(event=None):
    contenu()  

#Definition de la fonction pour afficher le menu    
def afficher_menu(event, menu):
    menu.post(event.x_root, event.y_root)

#Definition de la fonction pour l'option "ouvrir" dans le menu
def ouvrir(nom):
    if os.path.isdir(nom):
        naviguer_dossier(nom)
    else:
        try:
            os.startfile(nom)  
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le fichier : {e}")

#Definition de la fonction pour l'option "supprimer" dans le menu
def supprimer(nom):
    confirmation = messagebox.askyesno("Supprimer", f"Voulez-vous vraiment supprimer '{nom}' ?")
    if confirmation:
        try:
            if os.path.isdir(nom):
                os.rmdir(nom)  
            else:
                os.remove(nom)  
            contenu() 
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de supprimer '{nom}' : {e}")

#Definition de la fonction pour l'option"renommer"
def renommer(nom):
    nouveau_nom = simpledialog.askstring("Renommer", f"Nouveau nom pour '{nom}' :")
    if nouveau_nom:
        try:
            os.rename(nom, nouveau_nom)
            contenu() 
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de renommer '{nom}' : {e}")

#Definition de la fontion de navigation    
def naviguer_dossier(nom):
       if os.path.isdir(nom):
            try:
                  os.chdir(nom)  
                  chemin()  
                  contenu()
            except Exception as e:
                  messagebox.showerror("Erreur", f"Impossible d'accéder à ce dossier : {e}")            

#Definition de la fonction pour la surbrillance
def surbrillance(lbl):
    for widget in frame1.winfo_children():
        widget.config(bg="white", fg="black")  

    lbl.config(bg="blue", fg="white")

#Definition de la fonction pour créer un nouveau dossier
def creer_dossier():
    nom_dossier = simpledialog.askstring("Nouveau dossier", "Nom du nouveau dossier :")
    if nom_dossier:
        try:
            os.mkdir(nom_dossier)
            contenu()  
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de créer le dossier '{nom_dossier}' : {e}")

#Definition de la fonction pour le chemin
def chemin():
   chemin_actuel=os.getcwd()
   label2.config(text="")  
   label2.config(text=f"Chemin actuel : {chemin_actuel}")  
   label2.unbind("<Button-1>")
   label2.bind("<Button-1>", ouvrir_dossier)

#Definition de la fonction qui permet d'ouvrir le dossier en cliquant sur le chemin    
def ouvrir_dossier(event):
    chemin_actuel = label2.cget("text").replace("Chemin actuel : ", "").strip()
    if os.path.isdir(chemin_actuel):
        try:
            os.startfile(chemin_actuel)
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible d'ouvrir le dossier : {e}")

#Fonction de recherche
def rechercher():
    terme = entry.get().strip().lower() 
    fichiers = os.listdir(os.getcwd())  #liste les fichiers/dossiers du répertoire courant

    for widget in frame1.winfo_children():
        widget.destroy()  # Nettoie la liste avant d'afficher les résultats

    for fichier in fichiers:
        if terme in fichier.lower():  
            label = ttk.Label(frame1, text=fichier)
            label.grid(sticky=(W))
            label.bind("<Button-1>", lambda event, lbl=label: surbrillance(lbl))
            label.bind("<Double-1>", lambda event, nom=fichier: naviguer_dossier(nom) if os.path.isdir(nom) else ouvrir(nom))            

#Fonction  de retour 
def retour():
    os.chdir("..")  
    chemin()
    contenu()
    icone()
    
frame=ttk.Frame(root, borderwidth=2, relief="ridge")
frame.grid(padx=30, pady=10)

frame1=ttk.Frame(frame, borderwidth=2, relief="ridge", width=200, height=400)
frame1.grid(row=0, rowspan=3, column=0, padx=5, pady=5)
frame1.grid_propagate(False)
contenu()

frame2=ttk.Frame(frame, borderwidth=2, relief="ridge", width=1000, height=35)
frame2.grid(row=0, column=1, padx=5, pady=10, sticky=(N,S))
frame2.grid_propagate(False)

label2=ttk.Label(frame2, text="")
label2.grid(padx=5, pady=5)
chemin()

frame3=ttk.Frame(frame, borderwidth=1, relief="ridge", width=1000, height=300)
frame3.grid(row=2, column=1,padx=5, pady=5, sticky=(N,S))
frame3.grid_propagate(False)
icone()

bouton1= tk.Button(frame, text="Nouveau dossier", command=creer_dossier, bg="lightblue")
bouton1.grid(row=3, column=0, padx=5, pady=5, sticky=(W))

label1 = ttk.Label(frame2, text="Filtrer :")
label1.grid(row=0, column=1, padx=50, pady=5)

combo_filtre = ttk.Combobox(frame2, textvariable=filtre_selectionne, values=list(filtres.keys()), state="readonly")
combo_filtre.grid(row=0, column=3, padx=10, pady=5, sticky=(W))
combo_filtre.bind("<<ComboboxSelected>>", changer_filtre)

bouton2 = tk.Button(frame, text="Actualiser", command=contenu, bg="lightblue")
bouton2.grid( row=3, column=0, padx=20, pady=5, sticky=(S,E))

frame4=ttk.Frame(frame, borderwidth=2, relief="ridge", width=1000, height=35)
frame4.grid(row=1, column=1, padx=5, pady=10, sticky=(N,S))
frame4.grid_propagate(False)


label2 = ttk.Label(frame4, text="Rechercher :")
label2.grid(row=0, column=0, padx=5, pady=5)

entry = ttk.Entry(frame4, width=30)
entry.grid(row=0, column=1, padx=5, pady=5)
entry.bind("<KeyRelease>", lambda event: rechercher())  

bouton3 = tk.Button(frame, text="Retour", command=retour, bg="lightblue")
bouton3.grid(row=3, column=1, padx=5, pady=5, sticky="E")

bouton4 = tk.Button(frame, text="Favoris", command=afficher_favoris, bg="lightblue")
bouton4.grid(row=3, column=1, padx=5, pady=5, sticky=(S,W))





root.mainloop()
