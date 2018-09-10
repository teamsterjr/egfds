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
        'SELECT g.id, g.name, g.up, g.down, g.up - g.down as total, g.up + g.down as num_votes, ge.name as genre'
        ' FROM game g, genre ge where g.genre_id = ge.id'
        ' ORDER BY total desc, num_votes desc')