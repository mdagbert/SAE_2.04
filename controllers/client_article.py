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
    params = []
    mycursor.execute(sql, params)
    articles = mycursor.fetchall()

    # Récupérer les types d'articles pour les filtres
    sql_types = 'SELECT id_coupe_jean AS id_type_article, nom_coupe AS libelle FROM coupe_jean'
    mycursor.execute(sql_types)
    types_article = mycursor.fetchall()

    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           items_filtre=types_article)

