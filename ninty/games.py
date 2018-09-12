from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import pprint

from .db import get_db, query_db

bp = Blueprint('games', __name__)


@bp.route('/')
def index():
    return render_template('index.html', games=get_games())

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