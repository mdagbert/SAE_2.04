#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                        template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    db = get_db()
    mycursor = get_db().cursor()
    with open("/home/MathDriprio/SAE_2.04/sae_sql.sql", 'r', encoding='utf-8') as sql_file:
        sql_commands = sql_file.read()
    with mycursor as cursor:
        try:
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:
                    cursor.execute(command)
            db.commit()
            print("Database initialiser avec succès.")
        except Exception as e:
            db.rollback()
            print(f"Une erreur s'est produite lors de l'initialisation: {e}")


    get_db().commit()
    return redirect('/')
