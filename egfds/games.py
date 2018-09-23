from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from .db import get_db, query_db

bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route('/')
def recommendations():
    genres = query_db('select * from genre')
    return render_template('games/index.html', games=get_games(), genres=genres)

@bp.route('/games.json')
def ajax_games():
    return jsonify(get_games())

@bp.route('/<instanceId>/comments.json')
def ajax_comments(instanceId):
    comments = query_db(
            """
            SELECT      c.comment,
                        u.username,
                        v.date,
                        v.vote
            FROM        vote v
            LEFT JOIN   comment c
            ON          v.id=c.vote_id
            LEFT JOIN   user u
            ON          u.id = v.user_id
            WHERE v.instance_id=%s
            AND       c.comment != ''
            """,
            [int(instanceId)]
    )
    return jsonify(comments)

def get_votes(**kwargs):
    print(kwargs, flush=True)
    query = """
        SELECT      g.name as game,
                    c.comment,
                    u.username,
                    v.date,
                    v.vote
        FROM        vote v
        LEFT JOIN   comment c
        ON          c.vote_id = v.id
        LEFT JOIN   user u
        ON          u.id = v.user_id
        LEFT JOIN   game_instance gi
        ON          v.instance_id = gi.id
        LEFT JOIN   game g
        ON          g.id = gi.game_id
    """

    args=[]
    if kwargs['user']:
        query = query + ' WHERE v.user_id = %s'
        args.append(kwargs['user']['id'])


    return query_db(query, args)

def get_games():
    return query_db(
        """
        SELECT  g.id                    as game_id,
        gi.id                           as instance_id,
        g.name                          as name,
        COALESCE(SUM(c.vote=1),0)       as up,
        COALESCE(SUM(c.vote=-1),0)      as down,
        COALESCE(SUM(c.vote),0)         as total,
        COUNT(c.id)                     as num_votes,
        ge.name                         as genre
        FROM            game g
        LEFT join       genre ge on ge.id=g.genre_id
        LEFT join       game_instance gi on g.id=gi.game_id
        LEFT join       vote c on c.instance_id = gi.id
        GROUP BY        gi.id, g.id
        ORDER BY        total desc, num_votes desc
        """)