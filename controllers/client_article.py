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

    # Récupération des filtres de la session
    filter_word = session.get('filter_word', '')
    filter_types = session.get('filter_types', [])
    filter_prix_min = session.get('filter_prix_min', '')
    filter_prix_max = session.get('filter_prix_max', '')

    # Construction de la requête SQL avec filtres
    sql = """
        SELECT jean.id_jean AS id_article, jean.nom_jean AS nom, jean.prix_jean AS prix, 
               jean.photo AS image, jean.stock AS stock, coupe.nom_coupe AS type_article
        FROM jean
        LEFT JOIN coupe_jean coupe ON jean.coupe_jean_id = coupe.id_coupe_jean
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

    print(f"DEBUG SQL: {sql} | PARAMS: {params}")  # Debug SQL

    mycursor.execute(sql, tuple(params))
    articles = mycursor.fetchall()

    # Récupération des types pour le filtre
    mycursor.execute("SELECT id_coupe_jean, nom_coupe FROM coupe_jean")
    types_article = mycursor.fetchall()

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           items_filtre=types_article)

@client_article.route('/client/panier/filtre', methods=['POST'])
def filtre_panier():
    mycursor = get_db().cursor()

    # Récupération des filtres depuis le formulaire
    filter_word = request.form.get('filter_word', '').strip()
    filter_types = request.form.getlist('filter_types')
    filter_prix_min = request.form.get('filter_prix_min', '').strip()
    filter_prix_max = request.form.get('filter_prix_max', '').strip()

    # Sauvegarde des filtres en session
    session['filter_word'] = filter_word
    session['filter_types'] = filter_types
    session['filter_prix_min'] = filter_prix_min
    session['filter_prix_max'] = filter_prix_max

    return redirect('/client/article/show')

@client_article.route('/client/panier/filtre/suppr', methods=['POST'])
def reset_filtre():
    session.pop('filter_word', None)
    session.pop('filter_types', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    return redirect('/client/article/show')