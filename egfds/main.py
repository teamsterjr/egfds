import os
import collections
from flask import (redirect, url_for, send_from_directory, Blueprint)
from flask_assets import (Environment, Bundle)
from werkzeug.exceptions import abort
from .utils import populate_nav


bp = Blueprint('main', __name__)

def init_app(app):
    app.add_url_rule('/favicon.ico', endpoint='favicon')
    app.context_processor(default_sections)
    register_assets(app)

def register_assets(app):
    assets = Environment(app)
    js = Bundle('js/jquery.js', 'js/bootstrap.js', 'js/typeahead.js','js/datatables.js','js/egfds.js', filters='jsmin', output='gen/js/packed.js')
    assets.register('js_all', js)

    css = Bundle('css/bootstrap.min.css', 'css/datatables.min.css', 'css/style.css', output='gen/css/packed.css')
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