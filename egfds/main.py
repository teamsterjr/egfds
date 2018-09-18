from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
import collections

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    # flash('blah')
    return redirect(url_for('games.recommendations'))

def default_sections():
    sections = collections.OrderedDict()
    sections['/']={'name':"Home", 'url':'/', 'disabled':True}
    sections['/games']={'name':"Game Recommendations", 'url':'/games'}
    return sections

def render_with_nav(tmpl_name, this='/', sections=default_sections(), **kwargs):
    if(sections.get(this)):
        sections[this]["selected"]=True
    return render_template(tmpl_name, sections=sections, **kwargs)

def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def init_app(app):
    app.after_request(set_response_headers)