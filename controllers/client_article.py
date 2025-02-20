#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, Flask, request, render_template, redirect, abort, flash, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show', methods=['GET', 'POST'])
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

<<<<<<< HEAD

    sql = '''SELECT id_jean AS id_article, nom_jean AS nom, prix_jean AS prix, photo AS image FROM jean;'''
    params = []
    mycursor.execute(sql, params)
    articles = mycursor.fetchall()

    # Récupérer les types d'articles pour les filtres
    sql_types = 'SELECT id_coupe_jean AS id_type_article, nom_coupe AS libelle FROM coupe_jean'
    mycursor.execute(sql_types)
    types_article = mycursor.fetchall()
=======
    sql = '''SELECT 
                 jean.id_jean AS id_article,
            jean.nom_jean AS nom,
            jean.prix_jean AS prix,
            jean.photo AS image, 
            jean.stock AS stock
     FROM jean;'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    sql = ''' SELECT jean_id AS id_article,
                        utilisateur_id,
                        quantite_panier AS quantite,
                        jean.prix_jean AS prix,
                        jean.nom_jean AS nom
                        FROM ligne_panier 
                        JOIN jean ON jean.id_jean = ligne_panier.jean_id
                        WHERE utilisateur_id = %s ;'''
    mycursor.execute(sql, id_client)
    articles_panier = mycursor.fetchall()

    sql = ''' SELECT * FROM coupe_jean ; '''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()

    # Calcul du prix total du panier
    if len(articles_panier) >= 1:
        sql = ''' SELECT SUM(jean.prix_jean * ligne_panier.quantite_panier) AS prix_total FROM ligne_panier
                    JOIN jean ON ligne_panier.jean_id = jean.id_jean
                    WHERE utilisateur_id = %s ;'''
        mycursor.execute(sql, id_client)
        prix_total = mycursor.fetchone()['prix_total']
    else:
        prix_total = 0
>>>>>>> f4f293d5f437572395f632ff72b19faa37894b25

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
<<<<<<< HEAD
                           items_filtre=types_article)

=======
                           articles_panier=articles_panier,
                           prix_total=prix_total,
                           items_filtre=types_article
                           )
>>>>>>> f4f293d5f437572395f632ff72b19faa37894b25
