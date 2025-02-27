#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    quantite = request.form.get('quantite')
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s ; '''
    mycursor.execute(sql, (id_client, id_article))
    article_panier = mycursor.fetchone()
    print(id_client, id_article, quantite)

    mycursor.execute("SELECT * FROM jean WHERE id_jean = %s;", id_article)
    article = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite_panier'] >= 1:
        tuple_update = (quantite, id_client, id_article)
        sql = ''' UPDATE ligne_panier SET quantite_panier = quantite_panier+%s WHERE utilisateur_id = %s AND jean_id = %s ; '''
        mycursor.execute(sql, tuple_update)
    else:
        tuple_insert = (id_client, id_article, quantite)
        sql = ''' INSERT INTO ligne_panier(utilisateur_id, jean_id, quantite_panier, date_ajout) VALUES (%s, %s, %s, current_timestamp); '''
        mycursor.execute(sql, tuple_insert)

    tuple_update = (quantite, id_article)
    sql = ''' UPDATE jean SET stock = stock - %s WHERE id_jean = %s ; '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()

    # id_declinaison_article=request.form.get('id_declinaison_article',None)
    id_declinaison_article = 1

    # ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    # sql = '''    '''
    # mycursor.execute(sql, (id_article))
    # declinaisons = mycursor.fetchall()
    # if len(declinaisons) == 1:
    #     id_declinaison_article = declinaisons[0]['id_declinaison_article']
    # elif len(declinaisons) == 0:
    #     abort("pb nb de declinaison")
    # else:
    #     sql = '''   '''
    #     mycursor.execute(sql, (id_article))
    #     article = mycursor.fetchone()
    #     return render_template('client/boutique/declinaison_article.html'
    #                                , declinaisons=declinaisons
    #                                , quantite=quantite
    #                                , article=article)

    # ajout dans le panier d'un article

    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article', '')
    quantite = 1

    # ---------
    # partie 2 : on supprime une déclinaison de l'article
    # id_declinaison_article = request.form.get('id_declinaison_article', None)

    tuple_select = (id_client, id_article)
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s ;'''
    mycursor.execute(sql, tuple_select)
    article_panier = mycursor.fetchone()

    if not (article_panier is None) and article_panier['quantite_panier'] > 1:
        tuple_update = (quantite, id_client, id_article)
        sql = ''' UPDATE ligne_panier SET quantite_panier = quantite_panier-%s WHERE utilisateur_id = %s AND jean_id = %s ; '''
        mycursor.execute(sql, tuple_update)
    else:
        tuple_update = (id_client, id_article)
        sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s  AND jean_id = %s ; '''
        mycursor.execute(sql, tuple_update)

    # mise à jour du stock de l'article disponible
    tuple_update = (quantite, id_article)
    sql = ''' UPDATE jean SET stock = stock + %s WHERE id_jean = %s ; '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    mycursor.execute(''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s ; ''', client_id)
    items_panier = mycursor.fetchall()
    for item in items_panier:
        print(item)
        tuple_delete = (item['jean_id'], item['utilisateur_id'])
        sql = ''' DELETE FROM ligne_panier WHERE jean_id = %s AND utilisateur_id = %s ; '''
        mycursor.execute(sql, tuple_delete)

        tuple_update = (item['jean_id'], item['quantite_panier'])
        sql2 = ''' UPDATE jean SET stock = stock + %s WHERE id_jean = %s ; '''
        mycursor.execute(sql2, tuple_update)
        get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('id_article')
    # id_declinaison_article = request.form.get('id_declinaison_article')

    tuple_select = (id_client, id_article)
    sql = ''' SELECT * FROM ligne_panier WHERE utilisateur_id = %s AND jean_id = %s ; '''
    mycursor.execute(sql, tuple_select)
    ligne_panier = mycursor.fetchone()
    quantite = ligne_panier['quantite_panier']

    tuple_delete = (id_client, id_article)
    sql = ''' DELETE FROM ligne_panier WHERE utilisateur_id = %s  AND jean_id = %s ; '''
    mycursor.execute(sql, tuple_delete)
    tuple_update = (quantite, id_article)
    sql2 = ''' UPDATE jean SET stock = stock + %s WHERE id_jean = %s ; '''
    mycursor.execute(sql2, tuple_update)

    get_db().commit()
    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    print("suppr filtre")
    return redirect('/client/article/show')
