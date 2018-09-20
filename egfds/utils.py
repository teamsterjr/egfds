import functools
from datetime import datetime
import dateutil
from flask.json import JSONEncoder
from flask import redirect, url_for, g, config, request, current_app

def init_app(app):
    app.json_encoder = DateJSONEncoder
    app.add_template_filter(_jinja2_filter_datetime, 'strftime')
    app.after_request(set_response_headers)

def normalizeDate(obj):
    from_zone = dateutil.tz.gettz('UTC')
    to_zone = dateutil.tz.gettz('Europe/London')
    obj=obj.replace(tzinfo=from_zone)
    return obj.replace(tzinfo=from_zone).astimezone(to_zone)

def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('admin.login'))

        return view(**kwargs)

    return wrapped_view

def _jinja2_filter_datetime(date, fmt=None):
    native=normalizeDate(date)
    format='%c'
    return native.strftime(format)

def populate_nav(links=[], prefix='', **kwargs):
    current_path = request.path
    title = kwargs.get('title', current_app.config['SITE_NAME'])

    for link in links:
        link['url'] = '{}/{}'.format(prefix,link.get('url',''))
        if link.get('url') == current_path:
            link['selected']=True
            if link.get('title'):
                title = link['title']
    return {'sections':links, 'title':title}


class DateJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return normalizeDate(obj).strftime('%c')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return super().default(self, obj)