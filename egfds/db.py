from flask_mysqldb import MySQL
import MySQLdb

import os

import click
from flask import current_app, g
from flask.cli import with_appcontext

mysql = MySQL()

def get_cursor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    return cursor

def commit_db():
    mysql.connection.commit()

def query_db(query, args=(), one=False):
    cur = get_cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    mysql.init_app(app)