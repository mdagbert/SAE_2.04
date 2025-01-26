#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, Flask, request, render_template, redirect, abort, flash, session
from connexion_db import get_db

client_article = Blueprint('client_article', __name__, template_folder='templates')


@client_article.route('/client/index')
@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session.get('id_user')

    sql = '''SELECT 
                 jean.id_jean AS id_article,
            jean.nom_jean AS nom,
            jean.prix_jean AS prix,
            jean.stock AS stock,
            jean.photo AS image,
     FROM jean;'''
    mycursor.execute(sql)
    articles = mycursor.fetchall()

    # articles_panier = []
    # types_article = []

    # Calcul du prix total du panier
    # if len(articles_panier) >= 1:
    #     prix_total = sum(article['prix'] * article['quantite'] for article in articles_panier)
    # else:
    #     prix_total = 0

    # Rendu de la page
    return render_template('client/boutique/panier_article.html',
                           articles=articles,
                           # articles_panier=articles_panier,
                           prix_total=0,
                           # items_filtre=types_article
                           )
