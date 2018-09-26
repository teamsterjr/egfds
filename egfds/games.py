from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from .db import get_cursor, query_db

bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route('/')
def recommendations():
    genres = query_db('select * from genre')
    return render_template('games/index.html', games=get_games(), genres=genres)


@bp.route('/games.json')
def ajax_games():
    return jsonify({'data':get_games()})


@bp.route('/<instanceId>/comments.json')
def ajax_comments(instanceId):
    query = """
            SELECT      c.comment,
                        u.username,
                        v.date,
                        v.vote
            FROM        vote v
            LEFT JOIN   comment c
            ON          v.id=c.vote_id
            LEFT JOIN   user u
            ON          u.id = v.user_id
            WHERE
                        v.instance_id=%s
            AND         c.comment != ''
    """

    args = [int(instanceId)]
    comments = query_db(query, args)

    return jsonify(comments)

def get_votes(**kwargs):
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

    args = []
    conditions = []
    if kwargs.get('user'):
        conditions.append('v.user_id = %s')
        args.append(kwargs['user']['id'])

    if kwargs.get('instance_id'):
        conditions.append('gi.id = %s')
        args.append(kwargs['instance_id'])

    if kwargs.get('require_comment'):
        conditions.append('c.comment != ""')

    if conditions:
        query = " WHERE ".join([query, " AND ".join(conditions)])

    return query_db(query, args)

def get_games(single=False,**kwargs):
    query = """
    SELECT  g.id                    as game_id,
        gi.id                           as instance_id,
        g.name                          as name,
        COALESCE(SUM(v.vote=1),0)       as up,
        COALESCE(SUM(v.vote=-1),0)      as down,
        COALESCE(SUM(v.vote),0)         as total,
        COUNT(v.id)                     as num_votes,
        COUNT(c.id)                     as num_comments,
        ge.name                         as genre
        FROM            game g
        LEFT join       genre ge on ge.id=g.genre_id
        LEFT join       game_instance gi on g.id=gi.game_id
        LEFT join       vote v on v.instance_id = gi.id
        LEFT join       comment c on v.id = c.vote_id
    """

    args = []
    conditions = []
    if kwargs.get('instance_id'):
        conditions.append('gi.id = %s')
        args.append(kwargs['instance_id'])

    if conditions:
        query = " WHERE ".join([query, " AND ".join(conditions)])

    query = "".join([query, """
        GROUP BY        gi.id, g.id
        ORDER BY        total desc, num_votes desc
        """])

    return query_db(query, args, single)
