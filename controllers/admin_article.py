#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
from random import random
from flask import Blueprint, request, render_template, redirect, flash, url_for
from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__, template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()
    sql = '''
    SELECT j.id_jean AS id_article, j.nom_jean AS nom, j.prix_jean, j.photo, j.stock,
           # COUNT(DISTINCT c.id_commentaire) AS nb_commentaires_nouveaux,
           # COUNT(DISTINCT d.id_declinaison) AS nb_declinaisons,
           t.nom_taille AS libelle, j.coupe_jean_id AS type_article_id
    FROM jean j
    # LEFT JOIN commentaire c ON j.id_jean = c.id_jean AND c.lu = 0
    # LEFT JOIN declinaison d ON j.id_jean = d.jean_id
    LEFT JOIN taille t ON j.taille_id = t.id_taille
    GROUP BY j.id_jean, j.nom_jean, j.prix_jean, j.photo, j.stock, t.nom_taille, j.coupe_jean_id
    ORDER BY j.nom_jean ASC
    '''
    mycursor.execute(sql)
    articles = mycursor.fetchall()
    return render_template('admin/article/show_article.html', articles=articles)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    return render_template('admin/article/add_article.html')


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()
    nom = request.form.get('nom', '')
    prix = request.form.get('prix', '')
    description = request.form.get('description', '')
    image = request.files.get('image', '')

    filename = None
    if image:
        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))

    sql = '''INSERT INTO jean (nom_jean, prix_jean, description, photo) VALUES (%s, %s, %s, %s)'''
    tuple_add = (nom, prix, description, filename)
    mycursor.execute(sql, tuple_add)
    get_db().commit()

    flash(f'Article ajouté: {nom}', 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()

    sql = '''SELECT photo FROM jean WHERE id_jean = %s'''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()

    if article and article['photo']:
        os.remove(os.path.join('static/images/', article['photo']))

    sql = '''DELETE FROM jean WHERE id_jean = %s'''
    mycursor.execute(sql, (id_article,))
    get_db().commit()

    flash(f'Article supprimé, ID: {id_article}', 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    id_article = request.args.get('id_article')
    mycursor = get_db().cursor()
    sql = '''SELECT * FROM jean WHERE id_jean = %s'''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()

    sql = '''SELECT * FROM coupe_jean'''
    mycursor.execute(sql)
    types_article = mycursor.fetchall()
    # sql_declinaisons = '''
    # SELECT d.id_declinaison AS id_declinaison_article, d.stock,
    #        t.nom_taille AS libelle_taille, c.nom_couleur AS libelle_couleur
    # FROM declinaison d
    # LEFT JOIN taille t ON d.taille_id = t.id_taille
    # LEFT JOIN couleur c ON d.couleur_id = c.id_couleur
    # WHERE d.jean_id = %s
    # '''
    # mycursor.execute(sql_declinaisons, (id_article,))
    # declinaisons_article = mycursor.fetchall()
    declinaisons_article = []
    return render_template('admin/article/edit_article.html',
                           article=article,
                           declinaisons_article=declinaisons_article,
                           types_article=types_article)


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    id_article = request.form.get('id_article')
    nom = request.form.get('nom')
    prix = request.form.get('prix')
    description = request.form.get('description')
    stock = request.form.get('stock')
    image = request.files.get('image', '')

    sql = '''SELECT photo FROM jean WHERE id_jean = %s'''
    mycursor.execute(sql, (id_article,))
    article = mycursor.fetchone()
    image_nom = article['photo'] if article else None

    if image:
        if image_nom:
            os.remove(os.path.join('static/images/', image_nom))
        filename = 'img_upload_' + str(int(2147483647 * random())) + '.png'
        image.save(os.path.join('static/images/', filename))
        image_nom = filename

    sql = '''UPDATE jean SET nom_jean = %s, prix_jean = %s, description = %s, photo = %s, stock = %s WHERE id_jean = %s'''
    mycursor.execute(sql, (nom, prix, description, image_nom, stock, id_article))
    get_db().commit()

    flash(f'Article modifié: {nom}', 'alert-success')
    return redirect('/admin/article/show')
