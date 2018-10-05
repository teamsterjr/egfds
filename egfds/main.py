import os
import collections
from flask import (redirect, url_for, send_from_directory, Blueprint)
from flask_assets import (Environment, Bundle)
from werkzeug.exceptions import abort
from .utils import populate_nav


bp = Blueprint('main', __name__)

def init_app(app):
    app.add_url_rule('/favicon.ico', 'favicon',favicon)
    app.context_processor(default_sections)
    if app.config['DEBUG']:
        app.after_request(bust_cache)
    register_assets(app)

def register_assets(app):
    if app.config['DEBUG']:
        app.config['ASSETS_DEBUG'] = True

    assets = Environment(app)
    js = Bundle(
        'js/external/jquery.js',
        'js/external/bootstrap.js',
        'js/external/typeahead.js',
        'js/external/datatables.js',
        'js/gametable.js',
        'js/egfds.js',
        'js/admin.js',
        filters='jsmin',
        output='gen/js/packed.js'
    )
    assets.register('js_all', js)

    css = Bundle(
        'css/external/bootstrap.min.css',
        'css/external/datatables.min.css',
        'css/style.css',
        output='gen/css/packed.css'
    )
    assets.register('css_all', css)

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

def bust_cache(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response