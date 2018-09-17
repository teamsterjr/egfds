from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from .db import get_db, query_db
from .main import render_with_nav

bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route('/')
def recommendations():
    genres = query_db('select * from genre')
    return render_with_nav('games/index.html', this='/games', games=get_games(), genres=genres)

@bp.route('/games.json')
def ajax_games():
    return jsonify(get_games())

def get_games():
    return query_db(
        """
        SELECT  g.id                    as game_id,
        gi.id                           as instance_id,
        g.name                          as name,
        COALESCE(sum(c.up), 0)          as up,
        COALESCE(sum(c.down), 0)        as down,
        COALESCE(sum(c.up - c.down), 0) as total,
        COUNT(c.id)                     as num_votes,
        ge.name                         as genre
        FROM            game g
        LEFT join       genre ge on ge.id=g.genre_id
        LEFT join       game_instance gi on g.id=gi.game_id
        LEFT join       comment c on c.instance_id = gi.id
        GROUP BY        gi.id, g.id
        ORDER BY        total desc, num_votes desc
        """)