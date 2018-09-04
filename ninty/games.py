from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .db import get_db

bp = Blueprint('games', __name__)


@bp.route('/')
def index():
    db = get_db()
    games = db.execute(
        'SELECT g.name, g.up, g.down, g.up - g.down as total, g.up + g.down as num_votes, ge.name as genre'
        ' FROM games g, genres ge where g.genre_id = ge.id'
        ' ORDER BY total desc, num_votes desc'
    ).fetchall()

    return render_template('index.html', games=games)
