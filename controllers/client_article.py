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

    sql = '''SELECT id_jean AS id_article, nom_jean AS nom, prix_jean AS prix, photo AS image FROM jean;'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    # Récupérer les types d'articles pour les filtres
    sql_types = 'SELECT id_coupe_jean AS id_type_article, nom_coupe AS libelle FROM coupe_jean'
    mycursor.execute(sql_types)
    types_article = mycursor.fetchall()

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

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           items_filtre=types_article,
                           articles_panier=articles_panier,
                           prix_total=prix_total
                           )

@client_article.route('/client/panier/filtre', methods=['POST'])
def filtre_panier():
    mycursor = get_db().cursor()

    filter_word = request.form.get('filter_word', '').strip()
    filter_types = request.form.getlist('filter_types')
    filter_prix_min = request.form.get('filter_prix_min', '').strip()
    filter_prix_max = request.form.get('filter_prix_max', '').strip()

    session['filter_word'] = filter_word
    session['filter_types'] = filter_types
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max
    sql = """SELECT jean.id_jean AS id_article, jean.nom_jean AS nom, jean.prix_jean AS prix, 
               jean.photo AS image, jean.stock AS stock
        FROM jean;
    """
    conditions = []
    params = []

    if filter_word:
        conditions.append("jean.nom_jean LIKE %s")
        params.append(f"%{filter_word}%")

    if filter_types:
        placeholders = ', '.join(['%s'] * len(filter_types))
        conditions.append(f"jean.coupe_jean_id IN ({placeholders})")
        params.extend(filter_types)

    if filter_prix_min.isdigit():
        conditions.append("jean.prix_jean >= %s")
        params.append(filter_prix_min)

    if filter_prix_max.isdigit():
        conditions.append("jean.prix_jean <= %s")
        params.append(filter_prix_max)

    if conditions:
        sql += " WHERE " + " AND ".join(conditions)

    print(f"DEBUG SQL: {sql} | PARAMS: {params}")
    mycursor.execute(sql, tuple(params))
    articles = mycursor.fetchall()
    mycursor.execute("SELECT id_coupe_jean, nom_coupe FROM coupe_jean")
    types_article = mycursor.fetchall()
    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           items_filtre=types_article)

@client_article.route('/client/panier/filtre/suppr', methods=['POST'])
def reset_filtre():
    session.pop('filter_word', None)
    session.pop('filter_types', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    return redirect('/client/article/show')
