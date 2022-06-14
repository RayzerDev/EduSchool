#!/usr/bin/env python3
# coding: utf-8
"""
Usage: Application Gestion Elève
======
    python interface.py 

__authors__ = ("Louis KARAMUCKI")
__version__ = "1.0.0"
__copyright__ = "copyleft"
__date__ = "24/12/2021"

"""

# Modules externes
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
import shutil

# Connexion avec les fichiers
from db_manager import *

# Déclaration Class
class Fenetre(Tk):
    """
    """
    # Variables de Classe
    LOGO_ECOLE = 'image/logo_ecole.png'
    ICO_LOGO_ECOLE = 'image/icone_logo_ecole.ico'
    DIM_PHOTO = (40, 80)
    COLOR_BACK = '#E6FBF3'
    
    def __init__(self, titre, dim = (1280,720), color_bg = '#E6FBF3'):
        """
        :param (str): titre, Titre de la fenêtre
        :param (tuple): dim, Tuple avec les dimensions x et y
        """
        # Initialisation des variables
        self.dim, self.titre, self.color_bg, self.frame_active = dim, titre, color_bg, None
        
        # BDD
        self.bdd = DBManager()

        # Initialisation de la fenêtre
        Tk.__init__(self)
        self.config(menu = self.menu_bar())
        self.title(self.titre)
        dimension_fenetre = "%dx%d" % (self.dim[0], self.dim[1])
        self.geometry(dimension_fenetre)
        self['bg'] = self.color_bg
        self.iconbitmap(Fenetre.ICO_LOGO_ECOLE)

        self.onglet_accueil()

    def menu_bar(self):
        """
        """
        # Création du menu
        menu_bar = Menu(self)
        
        # Onglet Accueil
        menu_accueil = Menu(menu_bar, tearoff=0)
        menu_accueil.add_command(label="Retourner à l'accueil", command=self.onglet_accueil)
        menu_bar.add_cascade(label = 'Accueil', menu = menu_accueil)
        
        # Onglet Gestion Elève
        sous_menu_eleve = Menu(menu_bar, tearoff=0)
        sous_menu_eleve.add_command(label="Création fiche élève", command=self.onglet_fiche_eleve)
        sous_menu_eleve.add_command(label="Listing absence", command=self.onglet_listing_absence)
        sous_menu_eleve.add_command(label="Modifier fiche élève")
        menu_bar.add_cascade(label = 'Gestion élève', menu = sous_menu_eleve)
        
        # Gestion Classe
        sous_menu_classe = Menu(menu_bar, tearoff=0)
        sous_menu_classe.add_command(label="Création d'une classe", command=self.onglet_creation_classe)
        sous_menu_classe.add_command(label="Modifier une classe")
        sous_menu_classe.add_command(label="Trombinoscope", command=self.onglet_trombinoscope)
        menu_bar.add_cascade(label = 'Gestion classe', menu = sous_menu_classe)
        
        return menu_bar
            
    def frame_destroy(self):
        """
        Permets de supprimer la frame actuel et de passer à la frame voulu.
        """
        if self.frame_active:
            self.frame_active.destroy()
    
    def onglet_accueil(self):
        """
        """
        # Suppression de la frame précédente
        self.frame_destroy()
        
        # Mise en place de la frame d'accueil
        self.frame_accueil = Frame(self, borderwidth = 5, width = self.dim[0], height = self.dim[1], bg = Fenetre.COLOR_BACK)
        self.frame_active = self.frame_accueil
        self.frame_accueil.place(x= 0, y= 0)
        
        # Titre d'accueil
        self.texte = Label(self.frame_accueil, text =  "Bienvenue dans l'accueil ! \n Choisissez une option dans le menu déroulant.", font = ("Helvetica", 15), bg = self.color_bg)
        self.texte.place(x= self.dim[0]/2-self.texte.winfo_reqwidth()/2, y= 5)
        
    def onglet_fiche_eleve(self):
        """
        Frame graphique permettant l'enregistrement d'un élève dans la bdd
        """
        # Photo eleve destination
        self.photo_eleve_dest = 'image/photo_eleve/X.png'

        # Information
        self.l_info_eleve = ['Prénom', 'Nom', 'Année', 'Classe', 'Photo']

        #Liste Classe
        self.l_classe = self.bdd.get_liste_classe()
        self.l_intit_classe = [i[1] for i in self.l_classe]
        
        # Destruction ancienne frame
        self.frame_destroy()
        
        # Placement Frame
        self.frame_fiche_eleve = Frame(self, borderwidth = 5, width = self.dim[0], height = self.dim[1], bg = Fenetre.COLOR_BACK)
        self.frame_active = self.frame_fiche_eleve
        self.frame_fiche_eleve.place(x= 0, y= 0)
        
        # Titre
        self.texte = Label(self.frame_fiche_eleve, text =  "Création d'une fiche élève", font = ("Helvetica", 15), bg = self.color_bg)     
        self.texte.place(x= self.dim[0]/2-self.texte.winfo_reqwidth()/2, y= 5)

        # Photo
        self.img = Image.open(self.photo_eleve_dest)  
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.photo = Label(self, width = 60, height = 82)
        self.photo.configure(image = self.tkimage)
        self.photo.place(x = self.dim[0]/1.5, y = 165)      
        
        # Label Nom information
        self.l_w_info_eleve = []
        for i in range(len(self.l_info_eleve)):
            self.l_w_info_eleve.append(Label(self.frame_fiche_eleve, text = self.l_info_eleve[i], font = ("Helvetica", 15), bg = self.color_bg).place(x = 20, y = 160 + 50 * i))
        
        # Zone de saisie Prénom
        self.saisie_p = Entry(self.frame_fiche_eleve, width = 35)
        self.saisie_p.place(x= 140, y= 165)
        
        # Zone de saisie Nom
        self.saisie_n = Entry(self.frame_fiche_eleve, width = 35)
        self.saisie_n.place(x= 140, y= 215)

        # Zone de saisie Année
        self.saisie_a = Entry(self.frame_fiche_eleve, width = 35)
        self.saisie_a.place(x= 140, y= 265)
        
        # Menu des classes
        self.valeur_menu_c = StringVar(self.frame_fiche_eleve)
        self.valeur_menu_c.set('Sélectionnez une classe')
        self.menu_c = OptionMenu(self.frame_fiche_eleve, self.valeur_menu_c, *self.l_intit_classe)
        self.menu_c.place(x= 140, y= 310)
        
        # Upload image
        self.bouton_u = Button(self.frame_fiche_eleve, text = 'Télécharger votre photo', command = self.upload_image)
        self.bouton_u.place(x= 140, y= 361)
        
        # Bouton confirmation
        self.bouton_c = Button(self.frame_fiche_eleve, text = 'Enregistrer un nouvel élève', command = lambda: self.get_saisie_fiche_eleve(
            self.saisie_p.get(), self.saisie_n.get(), self.saisie_a.get(), self.valeur_menu_c.get(), self.photo_eleve_dest, self.l_classe))
        self.bouton_c.place(x= 140, y= 421)

    def get_saisie_fiche_eleve(self, prenom, nom, annee, classe, photo, l_classe_bdd):
        """
        Fonction récupérant les informations de l'onglet fiche élève afin de permettre l'enregistrement dans la BDD.
        Utilisable uniquement dans la méthode de la fiche élève.
        """
        # Test entrée ou pas 
        if not prenom or not nom or not annee :
            return showerror("Vous n'avez pas tout remplis !", "Vous devez compléter au moins le prenom, le nom et l'année.")
        
        # Test année conforme
        if len(annee) != 4:
            return showerror("Saisie incorrect", "Vous devez écrire l'année comme '2020'.")
        
        self.prenom, self.nom, self.annee, self.classe, self.photo = prenom, nom, annee, classe, photo
        
        # Classe choisis 
        if self.classe == 'Sélectionnez une classe':
            self.classe = None
            
        # Détermination de l'id de la classe
        self.id_classe = None
        for i in l_classe_bdd:
            if self.classe == i[1]:
                self.id_classe = i[0]

        self.check = self.bdd.set_eleve([self.prenom, self.nom, self.annee, self.id_classe, self.photo])

        if self.check: return showinfo("L'élève a bien été enregistré !", "L'enregistrement de l'élève dans la base de donnée !")

        return showerror("Erreur d'enregistrement", "L'élève n'a pas pu être enregistré dans la base de donnée. Contactez les administrateurs.")

    def upload_image(self):
        """
        Méthode qui permet de récupérer sur l'ordinateur et de la recadrer au format 118/162.
        """
        f_types = [('Jpeg Files', '*.jpeg'), ('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
        source = filedialog.askopenfilename( title = 'Choisissez votre photo ', filetypes = f_types)
        
        if not source: return
        
        photo = source.split("/")[-1:][0]
        self.photo_eleve_dest = shutil.copy(source, 'image/photo_eleve/' + photo)
        
        image = Image.open(self.photo_eleve_dest)
        resize_img = image.resize((60, 82))
        resize_img.save(self.photo_eleve_dest)
        
        self.tkimage = ImageTk.PhotoImage(resize_img)
        self.photo.configure(image = self.tkimage)
    
    def onglet_listing_absence(self):
        """
        Méthode créant une frame permettant de lister les absences des élèves ou d'enregistrer une absence.
        """
        #
        self.frame_destroy()
        
        #
        self.frame_listing_absence = Frame(self, borderwidth = 5, width = self.dim[0], height = self.dim[1], bg = Fenetre.COLOR_BACK)
        self.frame_active = self.frame_listing_absence
        self.frame_listing_absence.place(x= 0, y= 0)
        
        #
        self.texte = Label(self.frame_listing_absence, text =  "Listing des absences", font = ("Helvetica", 15), bg = self.color_bg)
        self.texte.place(x= self.dim[0]/2-self.texte.winfo_reqwidth()/2, y= 5)
        
    def onglet_creation_classe(self):
        """
        Frame graphique permettant l'enregistrement d'une classe dans la bdd
        """
        #
        self.frame_destroy()
        
        #
        self.frame_creation_classe = Frame(self, borderwidth = 5, width = self.dim[0], height = self.dim[1], bg = Fenetre.COLOR_BACK)
        self.frame_active = self.frame_creation_classe
        self.frame_creation_classe.place(x= 0, y= 0)
        
        #
        self.texte = Label(self.frame_creation_classe, text =  "Création d'une classe", font = ("Helvetica", 15), bg = self.color_bg)
        self.texte.place(x= self.dim[0]/2-self.texte.winfo_reqwidth()/2, y= 5)

        # Information
        self.l_info_classee = ['Nom de la classe', 'Année Scolaire']
        
        # Label Nom information
        self.l_w_info_classee = []
        for i in range(len(self.l_info_classee)):
            self.l_w_info_classee.append(Label(self.frame_creation_classe, text = self.l_info_classee[i], font = ("Helvetica", 15), bg = self.color_bg).place(x = 20, y = 160 + 50 * i))
        
        # Zone de saisie Prénom
        self.saisie_n = Entry(self.frame_creation_classe, width = 35)
        self.saisie_n.place(x= 180, y= 165)
        
        # Zone de saisie Nom
        self.saisie_a = Entry(self.frame_creation_classe, width = 35)
        self.saisie_a.place(x= 180, y= 215)
        
        # Menu des classes
        self.l_c = self.bdd.get_liste_classe()
        self.l_intit_c = [i[1] for i in self.l_c]
        
        self.valeur_menu_c = StringVar(self.frame_fiche_eleve)
        self.valeur_menu_c.set('Sélectionnez une classe')
        self.menu_c = OptionMenu(self.frame_creation_classe, self.valeur_menu_c, self.l_intit_c)
        self.menu_c.place(x= 180, y= 310)
                
        # Bouton confirmation
        self.bouton_c = Button(self.frame_creation_classe, text = 'Enregistrer une nouvelle classe', command = None )
        self.bouton_c.place(x= 140, y= 421)
        
    def get_saisie_fiche_classe(self, intitule, annee):
        """
        Fonction récupérant les informations de l'onglet fiche classe afin de permettre l'enregistrement dans la BDD.
        Utilisable uniquement dans la méthode de la fiche classe.
        """
        if not prenom or not nom or not annee :
            return showerror("Vous n'avez pas tout remplis !", "Vous devez compléter au moins le prenom, le nom et l'année.")

        if len(annee) != 4:
            return showerror("Saisie incorrect", "Vous devez écrire l'année comme '2020'.")
        
        self.intitule, self.anne = intitule, annee

        if self.classe == 'Sélectionnez une classe':
            self.classe = None

        self.id_classe = None
        
        for i in l_classe_bdd:
            if self.classe == i[1]:
                self.id_classe = i[0]

        self.check = self.bdd.set_eleve([self.prenom, self.nom, self.annee, self.id_classe, self.photo])

        if self.check: return showinfo("L'élève a bien été enregistré !", "L'enregistrement de l'élève dans la base de donnée !")

        return showerror("Erreur d'enregistrement", "L'élève n'a pas pu être enregistré dans la base de donnée. Contactez les administrateurs.")
    
    def onglet_trombinoscope(self):
        """
        """
        #
        self.trombinoscope_actif = None

        # Liste Classe
        self.l_classe = self.bdd.get_liste_classe()
        self.l_intit_classe = [i[1] for i in self.l_classe]
        self.l_annee_classe = [i[2] for i in self.l_classe]

        # Destruction de l'ancinenne frame
        self.frame_destroy()
        
        #
        self.frame_trombinoscope = Frame(self, borderwidth = 5, width = self.dim[0], height = self.dim[1], bg = Fenetre.COLOR_BACK)
        self.frame_active = self.frame_trombinoscope
        self.frame_trombinoscope.place(x= 0, y= 0)

        #
        self.frame_secondaire = None
        
        #
        self.texte = Label(self.frame_trombinoscope, text =  "Trombinoscope par classe", font = ("Helvetica", 15), bg = self.color_bg)
        self.texte.place(x= (self.dim[0]-self.texte.winfo_reqwidth())/2, y= 5)

        # Menu des classes
        self.valeur_menu_c = StringVar(self.frame_trombinoscope)
        self.valeur_menu_c.set('Sélectionnez une classe')
        self.menu_c = OptionMenu(self.frame_trombinoscope, self.valeur_menu_c, *self.l_intit_classe)
        self.menu_c.place(x= 70, y= 50)

        # Bouton de raffraichissement 
        self.bouton_r = Button(self.frame_trombinoscope, text = 'Raffraichir le trombinoscope', command = lambda:
                               self.frame_onglet_trompinoscope_affiche(self.frame_secondaire, self.l_classe, self.valeur_menu_c.get()) )
        self.bouton_r.place(x= self.dim[0]-200, y= 50)
        
    def frame_onglet_trompinoscope_affiche(self, frame, l_classe_bdd, intit_classe):
        """
        """
        if self.frame_secondaire: self.frame_secondaire.destroy()
        if self.trombinoscope_actif: del(self.trombinoscope_actif)

        if intit_classe == 'Sélectionnez une classe':
            return showerror("Vous n'avez pas selectionné de classe", "Vous devez choisir une classe afin d'afficher son trombinoscope")

        self.frame_secondaire = Frame(self.frame_active, borderwidth = 5, width = self.dim[0]-20, height = self.dim[1]-105)
        self.frame_secondaire.place(x= 5, y= 90)

        self.id_classe = None
        
        for i in l_classe_bdd:
            if intit_classe == i[1]:
                self.id_classe = i[0]

        liste_eleve = self.bdd.get_eleve_in_classe(self.id_classe)
        liste_objet_eleve = []

        for i in range(len(liste_eleve)):
            liste_objet_eleve.append(Eleve_trombinoscope(liste_eleve[i], self.frame_active, self.frame_secondaire, i))
            
        #print(self.frame_secondaire.winfo_reqwidth())

        self.mainloop()

class Eleve_trombinoscope():

    frame_fiche_eleve = None
    
    def __init__(self, l_inf_eleve, frame_principale, frame_trombinoscope, i):
        """
        """
        # BDD
        self.bdd = DBManager()
        self.id = l_inf_eleve[0]
        
        self.l_inf_eleve = l_inf_eleve
        self.frame_trombinoscope = frame_trombinoscope
        self.frame_principale = frame_principale
        self.i = i
        
        self.img = Image.open(self.l_inf_eleve[5])  
        self.tkimage = ImageTk.PhotoImage(self.img)

        self.color_bg = '#E6FBF3'
        
        self.afficher_tkinter()

    def afficher_tkinter(self):
        """
        """
        # Photo
        self.photo = Button(self.frame_trombinoscope, width = 60, height = 82, image = self.tkimage, command=self.affichage_fiche_eleve)
        self.photo.grid(row=0, column=self.i, padx = 10)
        
        # Prénom
        self.text_prenom_nom = Label(self.frame_trombinoscope, text = self.l_inf_eleve[1] + '\n' + self.l_inf_eleve[2], width = 10, font = ("Helvetica", 8), bg = self.color_bg, justify = "center")
        self.text_prenom_nom.grid(row=1, column=self.i, padx = 10)


    def affichage_fiche_eleve(self):
        """
        """
        if Eleve_trombinoscope.frame_fiche_eleve:
            Eleve_trombinoscope.frame_fiche_eleve.destroy()

        Eleve_trombinoscope.frame_fiche_eleve = Frame(self.frame_principale)
        Eleve_trombinoscope.frame_fiche_eleve.place(x= 500, y = 100)

        l_nom_info = {'Prénom':self.l_inf_eleve[1], 'Nom':self.l_inf_eleve[2],
                      'Année Scolaire': str(self.l_inf_eleve[3]),
                      'Classe':self.bdd.get_intit_classe(self.l_inf_eleve[4]),
                      'Absences':self.bdd.get_absences(self.id)}
        
        l_w_info_eleve = []
        
        for c,v in l_nom_info.items():
            l_w_info_eleve.append(Label(Eleve_trombinoscope.frame_fiche_eleve, text = c + ':   ' + str(v)).pack())
        