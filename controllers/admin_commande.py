#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, flash, session
from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__, template_folder='templates')


@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['GET', 'POST'])
def admin_commande_show():
    mycursor = get_db().cursor()
    id_commande = request.args.get('id_commande', None)

    # Récupération de toutes les commandes
    sql_commandes = '''
    SELECT c.id_commande, u.login, c.date_achat, c.etat_id, e.libelle,
           SUM(lc.quantite_commande) AS nbr_articles, SUM(lc.prix * lc.quantite_commande) AS prix_total
    FROM commande c
    JOIN utilisateur u ON c.utilisateur_id = u.id_utilisateur
    JOIN etat e ON c.etat_id = e.id_etat
    LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
    GROUP BY c.id_commande, u.login, c.date_achat, c.etat_id, e.libelle
    ORDER BY c.date_achat DESC'''
    mycursor.execute(sql_commandes)
    commandes = mycursor.fetchall()

    articles_commande = []
    commande_adresses = {}

    if id_commande:
        # Récupération des articles d'une commande spécifique
        sql_articles = '''
        SELECT j.nom_jean AS nom, lc.quantite_commande AS quantite, lc.prix, 
               (lc.quantite_commande * lc.prix) AS prix_ligne, c.etat_id, c.id_commande
        FROM ligne_commande lc
        JOIN jean j ON lc.jean_id = j.id_jean
        JOIN commande c ON lc.commande_id = c.id_commande
        WHERE lc.commande_id = %s'''
        mycursor.execute(sql_articles, (id_commande,))
        articles_commande = mycursor.fetchall()

        # Récupération des adresses de livraison et facturation
        sql_adresses = '''
        SELECT u.nom AS nom_livraison, u.nom AS nom_facturation,
               'adresse rue' AS rue_livraison, 'adresse rue' AS rue_facturation,
               '00000' AS code_postal_livraison, '00000' AS code_postal_facturation,
               'ville' AS ville_livraison, 'ville' AS ville_facturation,
               'adresse_identique' AS adresse_identique
        FROM utilisateur u
        JOIN commande c ON u.id_utilisateur = c.utilisateur_id
        WHERE c.id_commande = %s'''
        mycursor.execute(sql_adresses, (id_commande,))
        commande_adresses = mycursor.fetchone()
    print(commandes)
    return render_template('admin/commandes/show.html',
                           commandes=commandes,
                           articles_commande=articles_commande,
                           commande_adresses=commande_adresses)


@admin_commande.route('/admin/commande/valider', methods=['POST'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)

    if commande_id:
        sql_update = '''UPDATE commande SET etat_id = 2 WHERE id_commande = %s'''
        mycursor.execute(sql_update, (commande_id,))
        get_db().commit()
        flash("Commande validée et expédiée !", "success")

    return redirect('/admin/commande/show')
