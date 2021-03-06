from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app
)
from werkzeug.exceptions import abort

from .db import get_cursor, query_db
from urllib.parse import urlparse, parse_qs

bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route('/')
def recommendations():
    genres = query_db('select * from genre')
    return render_template('games/index.html', games=get_games(), genres=genres)


@bp.route('/games.json')
def ajax_games():
    return jsonify({'data':get_games()})

@bp.route('/<instance_id>/')
def show_game(instance_id):
    game = get_games(instance_id=instance_id, single=True, sort="name")
    votes = get_votes(instance_id=instance_id, require_comment=True)
    genres = query_db('select * from genre')
    links = get_links(instance_id=instance_id)
    return render_template("games/game.html", game=game, votes=votes, genres=genres, links=links, include_dismiss=True)

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
            LEFT JOIN   user_account u
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
        LEFT JOIN   user_account u
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
        conditions.append('c.comment is not null')

    if conditions:
        query = " WHERE ".join([query, " AND ".join(conditions)])
    return query_db(query, args)

def get_games(single=False,**kwargs):
    query = """
        SELECT  distinct g.id                    as game_id,
        gi.id                           as instance_id,
        g.name                          as name,
        string_agg(ge.name,', ' order by ge.id) as genre,
        coalesce(v.total,0) as total,
        coalesce(v.up,0) as up,
        coalesce(v.down,0) as down,
        coalesce(v.neutral,0) as neutral,
        coalesce(v.num_comments,0) as num_comments,
        coalesce(v.num_votes,0) as num_votes
        FROM            game g
        LEFT join       game_instance gi on g.id=gi.game_id
        LEFT join       game_genre gge on gge.game_id = g.id
        LEFT join       genre ge on ge.id=gge.genre_id
        LEFT join       (
            select v.instance_id,
                    SUM( CASE WHEN v.vote=1 THEN 1 END)  as up,
                    SUM( CASE WHEN v.vote=-1 THEN 1 END)  as down,
                    SUM( CASE WHEN v.vote=0 THEN 1 END)  as neutral,
                    SUM(v.vote)                     as total,
                    COUNT(v.id)                     as num_votes,
                    COUNT(c.id)                     as num_comments
              from vote v left join comment c on c.vote_id=v.id group by instance_id) as v on v.instance_id=gi.id
    """

    args = []
    conditions = []
    if kwargs.get('instance_id'):
        conditions.append('gi.id = %s')
        args.append(kwargs['instance_id'])

    if conditions:
        query = " WHERE ".join([query, " AND ".join(conditions)])

    query = "".join([query, """
        group by gi.id, g.id, v.total, v.up, v,down, v,neutral, v.num_comments, v.num_votes
        """])

    if kwargs.get('genre'):
        args.append(kwargs.get('genre'))
        query = "".join([query, """
            having %s = any(array_agg(ge.name))
            """])

    query = "".join([query, """
        ORDER BY        total desc, num_votes desc
        """])

    return query_db(query, args, single)

def get_links(**kwargs):
    query="""



        SELECT      lt.type as type,
                g.link,
                g.link_text,
                s.name as site,
                s.baseurl
        FROM        game_link g
        JOIN        game_link_type lt
        ON          (lt.id=g.link_type_id)
        JOIN        link_site s
        ON          (g.link_site=s.id)
        WHERE       game_instance_id=%s
    """
    links={}
    for link in query_db(query, [kwargs['instance_id']]):
        link_type = link.get('type')
        if not links.get(link_type):
            links[link_type] = []

        link['parsed']=urlparse(link['link'])
        link['qs']=parse_qs(link['parsed'].query)
        links[link_type].append(link)

    return links