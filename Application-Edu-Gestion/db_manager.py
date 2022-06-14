#!/usr/bin/env python3
# coding: utf-8
"""
Usage: Application Gestion Elève
======
    python db_manager.py 

__authors__ = ("Louis KARAMUCKI")
__version__ = "1.0.0"
__copyright__ = "copyleft"
__date__ = "24/12/2021"

"""

# Modules externes
import sqlite3

# Déclaration Class
class DBManager():
    # Variables de Classes
    """
    Méthode d'objet uniquement utilisable avec la bdd bdd_school_info.bdd
    """
    
    def __init__(self, arbo_fichier_db = 'bdd/bdd_school_info.db'):
        """
        Permet de gérer la base de donnée via python
        :param (str): Arbo base de donnée
        """
        # Connexion à la base
        self.arbo_fichier_db = arbo_fichier_db
        self.connexion = sqlite3.connect(self.arbo_fichier_db)
        
    def get_liste_eleve(self):
        """
        Obtenir la liste de tout les élèves de la table t_eleves
        :return (list): Liste de tuples des informations des élèves de la bdd
        :Effet de bord: None
        """
        try:
            self.curseur = self.connexion.cursor()
            self.curseur.execute('SELECT * FROM t_eleves')
            return self.curseur.fetchall()
        
        except:
            return False

    def get_liste_classe(self):
        """
        Obtenir la liste de toutes les classes de la table t_classes
        :return (list): Liste de tuples des informations des classes de la bdd
        :Effet de bord: None
        """
        try:
            self.curseur = self.connexion.cursor()
            self.curseur.execute('SELECT * FROM t_classes')
            return self.curseur.fetchall()

        except:
            return False

    def set_eleve(self, information_eleve):
        """
        Permets d'enregistrer un élève dans la base de donnée avec les informations en paramètres
        :param (list): information_eleve, liste avec les informations prénom(str), nom(str), annee_scolaire(int), id_classe(int), photo(str)
        :return (bool): Selon la réussite de l'insertion ou non
        :Effet de bord: Modification de la bdd
        """
        try:
            self.curseur = self.connexion.cursor()
            sql = 'INSERT INTO t_eleves(prenom, nom, annee_scolaire, id_classe, photo) VALUES(?,?,?,?,?)'
            self.curseur.execute(sql, information_eleve)
            self.connexion.commit()
            return True

        except:
            return False
    

    def get_eleve_in_classe(self, id_classe):
        """
        Obtenir la liste de tout les élèves d'une classe
        :param (int): id_classe de la table t_classes
        :return (list): liste des tuples des élèves de la classe
        :Effet de bord: None
        """
        self.curseur = self.connexion.cursor()
        sql = 'SELECT * FROM t_eleves WHERE id_classe = ?'
        self.curseur.execute(sql, str(id_classe))
        return self.curseur.fetchall()
    
    def set_classe(self, information_classe):
        """
        Permets d'enregistrer une classe dans la base de donnée avec les informations en paramètres
        :param (list): information_eleve, liste avec les informations intitule_classe(str), annee_scolaire(int)
        :return (bool): Selon la réussite de l'insertion ou non
        :Effet de bord: Modification de la bdd
        """
        try:
            self.curseur = self.connexion.cursor()
            sql = 'INSERT INTO t_classes(intitule_classe, annee_scolaire) VALUES(?,?)'
            self.curseur.execute(sql, information_classe)
            self.connexion.commit()
            return True
        
        except:
            return False
        
    def set_absence(self, information_absence):
        """
        Permets d'enregistrer une absence dans la base de donnée avec les informations en paramètres
        :param (list): information_eleve, liste avec les informations id_eleve(int), date(str)
        :return (bool): Selon la réussite de l'insertion ou non
        :Effet de bord: Modification de la bdd
        """
        try:
            self.curseur = self.connexion.cursor()
            sql = 'INSERT INTO t_abscences(id_eleve, date) VALUES(?,?)'
            self.curseur.execute(sql, information_absence)
            self.connexion.commit()
            return True
        
        except:
            return False
        
    def get_absences(self, id_eleve):
        """
        Permets d'obtenir les absences d'un élève dans la base de donnée avec l'id de l'élève
        :param (int): id_eleve, id de l'élève
        :return (list of tuple): Toutes les absences de l'élève
        :Effet de bord:
        """
        try:
            self.curseur = self.connexion.cursor()
            sql = 'SELECT * FROM t_abscences WHERE id_eleve = ?'
            self.curseur.execute(sql, id_eleve)
            return self.curseur.fetchall()
        
        except:
            return False
        
    def get_intit_classe(self, id_classe):
        """
        Permets d'obtenir l'intitulé d'une classe dans la base de donnée avec l'id de l'élève
        :param (int): id_classe, id de la classe
        :return (str): L'intitulé de la classe
        :Effet de bord:
        """
        try:
            self.curseur = self.connexion.cursor()
            sql = 'SELECT intitule_classe FROM t_classes WHERE id_classe = ?'
            self.curseur.execute(sql, [id_classe])
            return self.curseur.fetchall()[0][0]
        except:
            return False
