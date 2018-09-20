import os
import collections
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, send_from_directory
)
from werkzeug.exceptions import abort
from .utils import populate_nav

bp = Blueprint('main', __name__)

def init_app(app):
    app.add_url_rule('/favicon.ico', endpoint='favicon')
    app.context_processor(default_sections)

@bp.route('/')
def index():
    return redirect(url_for('games.recommendations'))

def default_sections():
    sections = [
        {'name':"Home", 'disabled':True},
        {'name':"Game Recommendations", 'url':'games/'}
    ]
    return populate_nav(links=sections)

def favicon():
    return send_from_directory(os.path.join(bp.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')