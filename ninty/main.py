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
    sections['/']={'name':"Home", 'url':'/'}
    sections['/games']={'name':"Game Recommendations", 'url':'/games'}
    return sections

def render_with_nav(tmpl_name, this='/', sections=default_sections(), **kwargs):
    print(sections)
    if(sections.get(this)):
        sections[this]["selected"]=True
    return render_template(tmpl_name, sections=sections, **kwargs)
