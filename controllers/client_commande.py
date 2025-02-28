#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, request, render_template, redirect, flash, session
from datetime import datetime
from connexion_db import get_db

client_commande = Blueprint('client_commande', __name__, template_folder='templates')


@client_commande.route('/client/commande/valide', methods=['POST'])
def client_commande_valide():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql_articles_panier = '''SELECT j.nom_jean AS nom, lp.quantite_panier AS quantite, j.prix_jean AS prix,
                             (lp.quantite_panier * j.prix_jean) AS prix_ligne
                             FROM ligne_panier lp
                             JOIN jean j ON lp.jean_id = j.id_jean
                             WHERE lp.utilisateur_id = %s'''
    mycursor.execute(sql_articles_panier, (id_client,))
    articles_panier = mycursor.fetchall()

    prix_total = sum(article['prix_ligne'] for article in articles_panier) if articles_panier else None

    # sql_adresses = '''SELECT * FROM adresse WHERE utilisateur_id = %s'''
    # mycursor.execute(sql_adresses, (id_client))
    # adresses = mycursor.fetchall()

    return render_template('client/boutique/panier_validation_adresses.html',
                           # adresses=adresses,
                           articles_panier=articles_panier,
                           prix_total=prix_total, validation=1)


@client_commande.route('/client/commande/add', methods=['POST'])
def client_commande_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_adresse_livraison = request.form.get('id_adresse_livraison')
    id_adresse_facturation = request.form.get('id_adresse_facturation')
    adresse_identique = request.form.get('adresse_identique')

    sql_panier = '''SELECT jean_id, quantite_panier, prix_jean FROM ligne_panier
                    JOIN jean ON ligne_panier.jean_id = jean.id_jean
                    WHERE utilisateur_id = %s'''
    mycursor.execute(sql_panier, (id_client,))
    items_ligne_panier = mycursor.fetchall()

    if not items_ligne_panier:
        flash(u'Pas d\'articles dans le panier', 'alert-warning')
        return redirect('/client/article/show')

    sql_commande = '''INSERT INTO commande (date_achat, utilisateur_id, etat_id) VALUES (NOW(), %s, 1)'''
    mycursor.execute(sql_commande, (id_client,))

    sql_last_id = '''SELECT last_insert_id() AS last_insert_id'''
    mycursor.execute(sql_last_id)
    id_commande = mycursor.fetchone()['last_insert_id']

    for item in items_ligne_panier:
        sql_ligne_commande = '''INSERT INTO ligne_commande (jean_id, commande_id, prix, quantite_commande)
                                 VALUES (%s, %s, %s, %s)'''
        mycursor.execute(sql_ligne_commande, (item['jean_id'], id_commande, item['prix_jean'], item['quantite_panier']))

    sql_delete_panier = '''DELETE FROM ligne_panier WHERE utilisateur_id = %s'''
    mycursor.execute(sql_delete_panier, (id_client,))
    get_db().commit()

    flash(u'Commande ajoutée', 'alert-success')
    return redirect('/client/article/show')


@client_commande.route('/client/commande/show', methods=['GET', 'POST'])
def client_commande_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']

    sql_commandes = '''SELECT c.id_commande, c.date_achat, e.libelle, c.etat_id,
                       COUNT(lc.jean_id) AS nbr_articles, SUM(lc.prix * lc.quantite_commande) AS prix_total
                       FROM commande c
                       JOIN etat e ON c.etat_id = e.id_etat
                       LEFT JOIN ligne_commande lc ON c.id_commande = lc.commande_id
                       WHERE c.utilisateur_id = %s
                       GROUP BY c.id_commande, c.date_achat, e.libelle, c.etat_id
                       ORDER BY c.etat_id ASC, c.date_achat DESC'''
    mycursor.execute(sql_commandes, (id_client))
    commandes = mycursor.fetchall()

    id_commande = request.args.get('id_commande')
    articles_commande = None
    commande_adresses = None

    if id_commande:
        sql_articles = '''SELECT j.nom_jean AS nom, lc.quantite_commande AS quantite, lc.prix, 
                          (lc.quantite_commande * lc.prix) AS prix_ligne, c.etat_id
                          FROM ligne_commande lc
                          JOIN jean j ON lc.jean_id = j.id_jean
                          JOIN commande c ON lc.commande_id = c.id_commande
                          WHERE lc.commande_id = %s'''
        mycursor.execute(sql_articles, (id_commande))
        articles_commande = mycursor.fetchall()

        # sql_adresses = '''SELECT * FROM adresse WHERE utilisateur_id = %s'''
        # mycursor.execute(sql_adresses, (id_client))
        # commande_adresses = mycursor.fetchone()

    return render_template('client/commandes/show.html',
                           commandes=commandes,
                           articles_commande=articles_commande
                           # ,commande_adresses=commande_adresses
                           )
